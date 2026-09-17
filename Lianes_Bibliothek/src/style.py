import streamlit as st
import base64
from pathlib import Path


def get_background_base64():
    """Lädt das Hintergrundbild und wandelt es in Base64 um. Gibt einen
    leeren String zurück, falls die Datei noch nicht existiert."""
    bg_path = Path(__file__).with_name("library_background.png")
    if bg_path.exists():
        return base64.b64encode(bg_path.read_bytes()).decode()
    return ""


def apply_design():
    background_image = get_background_base64()
    if background_image:
        bg_css = f'''linear-gradient(rgba(10, 8, 6, 0.3), rgba(12, 8, 5, 0.45)),
            url("data:image/png;base64,{background_image}") center center / cover scroll no-repeat'''
    else:
        bg_css = "linear-gradient(135deg, #12100E, #241A14)"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"], .stApp {{
     background: {bg_css} !important;
     color: #E8D8B4 !important;
    }}
    [data-testid="stHeader"] {{
     background: transparent !important;
    }}
    .block-container {{
     max-width: 1450px;
     padding-top: 1.2rem;
     padding-bottom: 5rem;
    }}
    html, body, .stApp, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
    .stRadio, .stSelectbox, .stTextInput, .stTextArea, .stNumberInput {{
     font-family: Georgia, "Times New Roman", serif !important;
    }}
    [data-testid="stMarkdownContainer"] p {{
     color: #E9DDBF !important;
    }}
    h1, h3 {{
        color: #D4B66A !important;
        font-family: Georgia, "Times New Roman", serif !important;
        text-shadow: 0 2px 4px #000, 0 0 18px rgba(201,164,92,0.18);
    }}
    h2 {{
        color: #D4B66A !important;
        font-family: Georgia, "Times New Roman", serif !important;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(201,164,92,0.45);
    }}
    .library-header {{
     text-align: center;
     padding: 32px 25px 34px 25px;
     margin-bottom: 20px;
     background: linear-gradient(135deg, rgba(28,20,15,0.90), rgba(15,12,10,0.92));
     border: 1px solid rgba(201,164,92,0.50);
     border-radius: 14px;
     box-shadow: 0 12px 30px rgba(0,0,0,0.42), inset 0 0 35px rgba(201,164,92,0.04);
    }}
    .library-exlibris {{
     color: #B9954F;
     letter-spacing: 9px;
     font-size: 14px;
     margin-bottom: 14px;
    }}
    .library-title {{
     color: #E1C06C;
     font-size: clamp(26px, 3vw, 40px);
     font-weight: bold;
     letter-spacing: 1px;
     line-height: 1.05;
     text-shadow: 0 4px 8px #000, 0 0 28px rgba(201,164,92,0.18);
    }}
    .library-subtitle {{
     color: #D8C6A0;
     font-size: 18px;
     font-style: italic;
     margin-top: 15px;
    }}
    .library-ornament {{
     color: #A98642;
     margin-top: 20px;
     font-size: 18px;
     letter-spacing: 7px;
    }}
    [data-testid="stMetric"] {{
     min-height: 70px;
     padding: 10px 16px !important;
     border-radius: 10px;
     border: 1px solid rgba(201,164,92,0.40);
     box-shadow: 0 8px 22px rgba(0,0,0,0.40);
    }}
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *,
    [data-testid="stMetric"] label, [data-testid="stMetric"] label * {{
     color: #F0E4C9 !important;
     font-weight: 600 !important;
     opacity: 1 !important;
    }}
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {{
     color: #F3D37A !important;
     font-weight: 700 !important;
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="column"] [data-testid="stColumn"] [data-testid="stMetric"] {{
     background: linear-gradient(145deg, rgba(38,58,85,0.94), rgba(20,30,45,0.96)) !important;
     border-top: 3px solid #587A9D;
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="column"] [data-testid="stColumn"] [data-testid="stMetric"] {{
     background: linear-gradient(145deg, rgba(116,86,30,0.94), rgba(55,42,18,0.96)) !important;
     border-top: 3px solid #C59A3B;
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="column"] [data-testid="stColumn"] [data-testid="stMetric"] {{
     background: linear-gradient(145deg, rgba(35,70,55,0.94), rgba(20,40,32,0.96)) !important;
     border-top: 3px solid #52795E;
    }}
    [data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="column"] [data-testid="stColumn"] [data-testid="stMetric"] {{
     background: linear-gradient(145deg, rgba(107,30,38,0.94), rgba(55,18,22,0.96)) !important;
     border-top: 3px solid #A74C57;
    }}
    [data-testid="stSidebar"] {{
     background: linear-gradient(180deg, rgba(18,15,13,0.97), rgba(10,8,6,0.98)) !important;
     border-right: 1px solid rgba(201,164,92,0.35);
     min-width: 320px !important;
     width: 320px !important;
    }}
    [data-testid="stSidebar"] * {{
     color: #E8D8B4 !important;
    }}
    div[role="radiogroup"] {{
     background: linear-gradient(90deg, rgba(30,22,17,0.96), rgba(18,15,13,0.96));
     border: 1px solid rgba(201,164,92,0.50);
     border-radius: 10px;
     padding: 14px 18px;
     margin: 25px 0 35px 0;
     box-shadow: 0 7px 18px rgba(0,0,0,0.42);
    }}
    div[role="radiogroup"] label, div[role="radiogroup"] label *,
    div[role="radiogroup"] p, div[role="radiogroup"] span {{
     color: #EBDDBE !important;
     opacity: 1 !important;
     font-weight: 600 !important;
     font-size: 16px !important;
    }}
    div[role="radiogroup"] label {{
     white-space: nowrap;
    }}
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] *,
    .stTextInput label, .stTextInput label *, .stTextArea label, .stTextArea label *,
    .stNumberInput label, .stNumberInput label *, .stSelectbox label, .stSelectbox label * {{
     color: #E6D4AE !important;
     opacity: 1 !important;
     font-weight: 600 !important;
    }}
    .stTextInput input, .stTextArea textarea, .stNumberInput input {{
     background: #E5D3AB !important;
     color: #241A14 !important;
     border: 1px solid #A88547 !important;
     border-radius: 7px !important;
     font-family: Georgia, "Times New Roman", serif !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {{
     border: 1px solid #D1AC5A !important;
     box-shadow: 0 0 0 1px rgba(209,172,90,0.35) !important;
    }}
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
     color: #756348 !important;
     opacity: 1 !important;
    }}
    div[data-baseweb="select"] > div {{
     background: #E5D3AB !important;
     border: 1px solid #A88547 !important;
     border-radius: 7px !important;
     color: #241A14 !important;
    }}
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
     color: #241A14 !important;
    }}
    .stButton > button, .stFormSubmitButton > button {{
     background: linear-gradient(180deg, #77571F 0%, #5A3E19 55%, #3C2914 100%) !important;
     color: #F6E7C4 !important;
     border: 1px solid #C7A154 !important;
     border-radius: 7px !important;
     padding: 0.55rem 1.2rem !important;
     font-family: Georgia, "Times New Roman", serif !important;
     font-weight: bold !important;
     box-shadow: 0 4px 12px rgba(0,0,0,0.40);
     transition: all 0.2s ease;
    }}
    .stButton > button *, .stFormSubmitButton > button * {{
     color: #F6E7C4 !important;
    }}
    .stButton > button:hover, .stFormSubmitButton > button:hover {{
     background: linear-gradient(180deg, #927031 0%, #67491E 55%, #463018 100%) !important;
     border-color: #E0C06D !important;
     transform: translateY(-1px);
     box-shadow: 0 6px 15px rgba(0,0,0,0.48);
    }}
    hr {{
     border-color: rgba(201,164,92,0.38) !important;
    }}
    .book-card {{
     background: linear-gradient(135deg, rgba(44,32,24,0.97), rgba(26,20,16,0.97));
     border: 1px solid rgba(201,164,92,0.38);
     border-left: 5px solid #C9A45C;
     border-radius: 9px;
     padding: 22px 24px;
     margin-bottom: 18px;
     min-height: 180px;
     box-shadow: 0 8px 22px rgba(0,0,0,0.44);
     position: relative;
    }}
    .book-card:after {{
     content: "✦";
     position: absolute;
     right: 18px;
     top: 13px;
     color: rgba(225,190,110,0.35);
     font-size: 20px;
    }}
    .book-title {{
     color: #E6C873;
     font-size: 23px;
     font-weight: bold;
     padding-right: 30px;
    }}
    .book-author {{
     color: #D9C6A1;
     font-style: italic;
     margin-top: 8px;
     font-size: 16px;
    }}
    .book-info {{
     color: #BEA477;
     margin-top: 20px;
    }}
    .book-available {{
     color: #7FA88D;
     margin-top: 17px;
     font-weight: bold;
    }}
    .book-borrowed {{
     color: #D49A68;
     margin-top: 17px;
     font-weight: bold;
    }}
    .reader-card {{
     background: linear-gradient(135deg, rgba(38,30,23,0.97), rgba(23,18,15,0.97));
     border: 1px solid rgba(201,164,92,0.35);
     border-radius: 9px;
     padding: 19px 22px;
     margin-bottom: 13px;
     box-shadow: 0 6px 16px rgba(0,0,0,0.38);
    }}
    .reader-name {{
     color: #DFC36E;
     font-size: 20px;
     font-weight: bold;
    }}
    .reader-contact {{
     color: #D8C7A7;
     margin-top: 8px;
    }}
    .overdue-card {{
     background: linear-gradient(135deg, rgba(83,27,32,0.95), rgba(42,18,20,0.96));
     border: 1px solid #87434B;
     border-left: 6px solid #B65760;
     border-radius: 9px;
     padding: 21px 24px;
     margin-bottom: 15px;
     box-shadow: 0 8px 20px rgba(0,0,0,0.42);
    }}
    .overdue-title {{
     color: #E6C16E;
     font-size: 21px;
     font-weight: bold;
    }}
    .overdue-person {{
     color: #E8DAC1;
     margin-top: 8px;
    }}
    .overdue-date {{
     color: #E59889;
     margin-top: 10px;
     font-weight: bold;
    }}
    .magic-info {{
     background: linear-gradient(90deg, rgba(36,27,20,0.96), rgba(23,19,16,0.96));
     border: 1px solid rgba(201,164,92,0.40);
     border-left: 4px solid #C9A45C;
     border-radius: 8px;
     padding: 16px 20px;
     margin-bottom: 24px;
     color: #E5D4B1;
     font-style: italic;
    }}
    [data-testid="stAlert"] {{
     border-radius: 8px !important;
     border: 1px solid rgba(201,164,92,0.30) !important;
    }}
    .library-footer {{
     text-align: center;
     color: #A98C5B;
     font-style: italic;
     padding-top: 45px;
     font-size: 14px;
     letter-spacing: 1px;
    }}
    </style>
    """, unsafe_allow_html=True)


def show_header():
    header_html = (
        '<div class="library-header">'
        '<div class="library-exlibris">✦ THE LIBRARY ✦</div>'
        '<div class="library-title">■ Lianes private Bibliothek</div>'
        '<div class="library-subtitle">'
        'Eine Sammlung voller Geschichten, Geheimnisse und vergessener Welten'
        '</div>'
        '<div class="library-ornament">■■■■ ■ ✦ ■ ■■■■</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)