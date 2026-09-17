import streamlit as st
import pandas as pd
from crud_functions import (
    buch_suchen, buch_ausleihen, buch_zurueckgeben, buch_loeschen,
    buch_hinzufuegen, ausleiher_hinzufuegen,
    alle_buecher, alle_ausleiher, alle_autoren, alle_buecher_detailliert,
    ausleihen_pro_ausleiher, kontakt_aktualisieren,
    abgeschlossene_ausleihen, ausleihe_loeschen, alle_ausleihen_uebersicht
)
from style import apply_design, show_header

st.set_page_config(page_title="Lianes Bibliothek", layout="wide")
apply_design()
show_header()

with st.sidebar:
    menu = st.radio("Navigation", [
        "Übersicht", "Bücherregal", "Buch suchen",
        "Buch hinzufügen", "Kontakt hinzufügen",
        "Buch ausleihen", "Buch zurückgeben", "Buch löschen",
        "Buch ausgeliehen an:", "Kontaktdaten aktualisieren",
        "Ausleihe zurück, löschen"
    ])

if menu == "Übersicht":
    st.header("Übersicht: Alle Ausleihen")
    ausleihen = alle_ausleihen_uebersicht()
    if ausleihen:
        df = pd.DataFrame([dict(row._mapping) for row in ausleihen])
        df_styled = df.style.set_properties(**{
            'background-color': '#241A14',
            'color': '#E8D8B4',
            'border-color': '#C9A45C'
        })
        st.dataframe(df_styled, use_container_width=True)
    else:
        st.write("Noch keine Ausleihen vorhanden.")

elif menu == "Bücherregal":
    st.header("Bücherregal")
    buecher = alle_buecher_detailliert()

    gesamt = len(buecher)
    verliehen_anzahl = sum(1 for b in buecher if b.verliehen)
    verfuegbar_anzahl = gesamt - verliehen_anzahl
    genres = sorted(set(b.genre for b in buecher if b.genre))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bücher gesamt", gesamt)
    col2.metric("Verfügbar", verfuegbar_anzahl)
    col3.metric("Verliehen", verliehen_anzahl)
    col4.metric("Genres", len(genres))

    genre_filter = st.selectbox("Genre filtern", ["Alle"] + genres)
    gefiltert = [b for b in buecher if genre_filter == "Alle" or b.genre == genre_filter]

    for buch in gefiltert:
        status_class = "book-borrowed" if buch.verliehen else "book-available"
        status_text = "Verliehen" if buch.verliehen else "Verfügbar"
        autor = f"{buch.first_name or ''} {buch.last_name or ''}".strip() or "Unbekannt"
        st.markdown(f"""
        <div class="book-card">
            <div class="book-title">{buch.title}</div>
            <div class="book-author">{autor}</div>
            <div class="book-info">Genre: {buch.genre or 'Unbekannt'}</div>
            <div class="{status_class}">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

elif menu == "Buch suchen":
    st.header("Buch suchen")
    suchbegriff = st.text_input("Buchtitel eingeben")
    if suchbegriff:
        ergebnisse = buch_suchen(suchbegriff)
        if ergebnisse:
            for buch in ergebnisse:
                st.write(buch)
        else:
            st.write("Kein Buch gefunden.")

elif menu == "Buch hinzufügen":
    st.header("Neues Buch hinzufügen")
    autoren = alle_autoren()

    with st.form(key='buch_hinzufuegen_form'):
        autor_auswahl = st.selectbox("Autor", autoren, format_func=lambda a: f"{a.first_name} {a.last_name}")
        titel = st.text_input("Titel")
        genre = st.text_input("Genre")
        isbn = st.text_input("ISBN")
        jahr = st.number_input("Erscheinungsjahr", min_value=1000, max_value=2100, step=1, value=2024)
        sprache = st.text_input("Sprache (z. B. ger)")
        verlag = st.text_input("Verlag")
        submitted = st.form_submit_button("Hinzufügen")

    if submitted:
        buch_hinzufuegen(autor_auswahl.authorID, titel, genre, isbn, jahr, sprache, verlag)
        st.success(f"'{titel}' erfolgreich hinzugefügt.")

elif menu == "Kontakt hinzufügen":
    st.header("Neuen Ausleiher hinzufügen")
    with st.form(key='kontakt_hinzufuegen_form'):
        vorname = st.text_input("Vorname")
        nachname = st.text_input("Nachname")
        email = st.text_input("E-Mail")
        telefon = st.text_input("Telefonnummer")
        submitted = st.form_submit_button("Hinzufügen")

    if submitted:
        ausleiher_hinzufuegen(vorname, nachname, email, telefon)
        st.success(f"'{vorname} {nachname}' erfolgreich hinzugefügt.")

elif menu == "Buch ausleihen":
    st.header("Buch ausleihen")
    buecher = alle_buecher()
    ausleiher = alle_ausleiher()

    with st.form(key='ausleihen_form'):
        buch_auswahl = st.selectbox("Buch", buecher, format_func=lambda b: f"{b.title} (ID {b.bookID})")
        ausleiher_auswahl = st.selectbox("Ausleiher", ausleiher, format_func=lambda a: f"{a.first_name} {a.last_name}")
        submitted = st.form_submit_button("Ausleihen")

    if submitted:
        erfolg = buch_ausleihen(buch_auswahl.bookID, ausleiher_auswahl.borrowerID)
        if erfolg:
            st.success(f"'{buch_auswahl.title}' erfolgreich ausgeliehen.")
        else:
            st.warning(f"'{buch_auswahl.title}' ist bereits verliehen.")

elif menu == "Buch zurückgeben":
    st.header("Buch zurückgeben")
    buecher = alle_buecher()

    with st.form(key='rueckgabe_form'):
        buch_auswahl = st.selectbox("Buch", buecher, format_func=lambda b: f"{b.title} (ID {b.bookID})")
        submitted = st.form_submit_button("Zurückgeben")

    if submitted:
        erfolg = buch_zurueckgeben(buch_auswahl.bookID)
        if erfolg:
            st.success(f"'{buch_auswahl.title}' als zurückgegeben markiert.")
        else:
            st.warning(f"Kein offener Loan für '{buch_auswahl.title}' gefunden.")

elif menu == "Buch löschen":
    st.header("Buch löschen")
    buecher = alle_buecher()

    with st.form(key='loeschen_form'):
        buch_auswahl = st.selectbox("Buch", buecher, format_func=lambda b: f"{b.title} (ID {b.bookID})")
        submitted = st.form_submit_button("Löschen")

    if submitted:
        erfolg = buch_loeschen(buch_auswahl.bookID)
        if erfolg:
            st.success(f"'{buch_auswahl.title}' erfolgreich gelöscht.")
        else:
            st.warning(f"'{buch_auswahl.title}' konnte nicht gelöscht werden (evtl. aktuell verliehen).")

elif menu == "Buch ausgeliehen an:":
    st.header("Buch ausgeliehen an:")
    ausleiher = alle_ausleiher()

    ausleiher_auswahl = st.selectbox("Ausleiher", ausleiher, format_func=lambda a: f"{a.first_name} {a.last_name}")

    if ausleiher_auswahl:
        offene_ausleihen = ausleihen_pro_ausleiher(ausleiher_auswahl.borrowerID)
        if offene_ausleihen:
            for ausleihe in offene_ausleihen:
                st.write(f"{ausleihe.title} — ausgeliehen seit {ausleihe.loan_date}")
        else:
            st.write("Keine aktuell offenen Ausleihen.")

elif menu == "Kontaktdaten aktualisieren":
    st.header("Kontaktdaten aktualisieren")
    ausleiher = alle_ausleiher()

    with st.form(key='kontakt_form'):
        ausleiher_auswahl = st.selectbox("Ausleiher", ausleiher, format_func=lambda a: f"{a.first_name} {a.last_name}")
        neue_email = st.text_input("E-Mail")
        neue_telefonnummer = st.text_input("Telefonnummer")
        submitted = st.form_submit_button("Aktualisieren")

    if submitted:
        erfolg = kontakt_aktualisieren(ausleiher_auswahl.borrowerID, neue_email, neue_telefonnummer)
        if erfolg:
            st.success(f"Kontaktdaten für {ausleiher_auswahl.first_name} {ausleiher_auswahl.last_name} aktualisiert.")
        else:
            st.warning("Ausleiher nicht gefunden.")

elif menu == "Ausleihe zurück, löschen":
    st.header("Abgeschlossene Ausleihe löschen")
    ausleihen = abgeschlossene_ausleihen()

    if not ausleihen:
        st.write("Keine abgeschlossenen Ausleihen vorhanden.")
    else:
        with st.form(key='ausleihe_loeschen_form'):
            ausleihe_auswahl = st.selectbox(
                "Ausleihe",
                ausleihen,
                format_func=lambda a: f"{a.title} — {a.first_name} {a.last_name} (zurückgegeben am {a.return_date})"
            )
            submitted = st.form_submit_button("Löschen")

        if submitted:
            erfolg = ausleihe_loeschen(ausleihe_auswahl.loanID)
            if erfolg:
                st.success("Ausleihe-Eintrag erfolgreich gelöscht.")
            else:
                st.warning("Ausleihe konnte nicht gelöscht werden.")