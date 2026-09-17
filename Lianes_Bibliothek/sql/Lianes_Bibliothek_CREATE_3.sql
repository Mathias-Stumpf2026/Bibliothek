-- =====================================================================
-- Lianes Bibliothek – Datenbankmodell
-- Basis: Lianes-DB-design.mwb (MySQL Workbench, Schema "mydb")
-- Überarbeitet auf Basis eines Vergleichs mit dem Schulskript
-- (5_create_schema_beispiel.sql): ergänzt um loan_date-Default,
-- due_date, loan_status, max_loans sowie fachlich passendere
-- ON DELETE/ON UPDATE-Regeln.
-- Stand: 10.09.2026
-- Zeile für Zeile kommentiert.
-- =====================================================================

-- Aktuellen Wert von UNIQUE_CHECKS in einer Session-Variable sichern und danach abschalten,
-- damit beim Anlegen der Tabellen keine Unique-Prüfungen die Reihenfolge stören.
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;

-- Aktuellen Wert von FOREIGN_KEY_CHECKS sichern und danach abschalten,
-- damit Tabellen mit Fremdschlüsseln unabhängig von der Erstellreihenfolge angelegt werden können.
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Aktuellen SQL_MODE sichern und auf TRADITIONAL + ALLOW_INVALID_DATES setzen
-- (Standardverhalten von MySQL-Workbench-Exportskripten, u. a. für YEAR/DATE-Spalten).
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- Schema "mydb" anlegen, falls es noch nicht existiert, mit Zeichensatz utf8mb4
-- (unterstützt Umlaute, Sonderzeichen und Emojis vollständig).
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb4;

-- Ab hier alle nachfolgenden Befehle auf das Schema "mydb" anwenden,
-- ohne den Schemanamen bei jeder Tabelle erneut angeben zu müssen.
USE `mydb`;

-- -----------------------------------------------------
-- Tabelle `authors`
-- -----------------------------------------------------

-- Tabelle "authors" anlegen, falls sie noch nicht existiert. Sie speichert die Stammdaten der Buchautoren
-- (normalisiert gegenüber dem Schulskript, das den Autor als reines Textfeld in books führt).
CREATE TABLE IF NOT EXISTS `mydb`.`authors` (
  -- Eindeutige, automatisch hochzählende ID des Autors (Primärschlüssel).
  `authorID` INT NOT NULL AUTO_INCREMENT,
  -- Vorname des Autors; optional, da z. B. bei Pseudonymen nicht immer vorhanden.
  `first_name` VARCHAR(45) NULL,
  -- Nachname des Autors; Pflichtfeld, da zur eindeutigen Identifikation benötigt.
  `last_name` VARCHAR(60) NOT NULL,
  -- authorID als Primärschlüssel der Tabelle festlegen.
  PRIMARY KEY (`authorID`)
-- Speicher-Engine InnoDB verwenden (unterstützt Fremdschlüssel und Transaktionen).
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabelle `books`
-- -----------------------------------------------------

-- Tabelle "books" anlegen, falls sie noch nicht existiert. Sie speichert die Bücher im Bestand.
CREATE TABLE IF NOT EXISTS `mydb`.`books` (
  -- Eindeutige, automatisch hochzählende ID des Buchs (Primärschlüssel).
  `bookID` INT NOT NULL AUTO_INCREMENT,
  -- Verweis auf den Autor (Fremdschlüssel zu authors.authorID); Pflichtfeld, jedes Buch braucht einen Autor.
  `authorID` INT NOT NULL,
  -- Buchtitel; Pflichtfeld.
  `title` VARCHAR(255) NOT NULL,
  -- Untertitel des Buchs; optional.
  `subtitle` VARCHAR(255) NULL,
  -- Kurzbeschreibung / Klappentext; optional, als TEXT für längere Inhalte.
  `description` TEXT NULL,
  -- Genre bzw. Kategorie des Buchs; optional.
  `genre` VARCHAR(45) NULL,
  -- Pfad oder URL zum Cover-Bild; optional.
  `cover` VARCHAR(255) NULL,
  -- ISBN-Nummer des Buchs; optional, Länge 17 deckt ISBN-13 inkl. Bindestrichen ab.
  `ISBN` VARCHAR(17) NULL,
  -- Erscheinungsjahr des Buchs; optional, MySQL-Datentyp YEAR.
  `pub_year` YEAR NULL,
  -- Kennzeichnung für Mehrfachexemplare; optional, Bedeutung im Modell nicht näher spezifiziert.
  `duplicate` VARCHAR(45) NULL,
  -- Sprachcode des Buchs (z. B. DEU, ENG); optional, 3-stelliges Kürzel.
  `language` CHAR(3) NULL,
  -- Verlag des Buchs; optional.
  `verlag` VARCHAR(45) NULL,
  -- bookID als Primärschlüssel der Tabelle festlegen.
  PRIMARY KEY (`bookID`),
  -- Index auf authorID anlegen, um Joins/Lookups über den Fremdschlüssel zu beschleunigen.
  INDEX `fk_books_authors1_idx` (`authorID` ASC) VISIBLE,
  -- Fremdschlüssel-Constraint: authorID muss auf einen existierenden Eintrag in authors.authorID verweisen.
  CONSTRAINT `fk_books_authors1`
    FOREIGN KEY (`authorID`)
    REFERENCES `mydb`.`authors` (`authorID`)
    -- Übernommen aus dem Schulskript: Wird ein Autor gelöscht, sollen auch seine Bücher automatisch
    -- mitgelöscht werden, damit keine verwaisten authorID-Verweise entstehen.
    ON DELETE CASCADE
    -- Ändert sich die authorID (z. B. bei einer Korrektur), wird sie automatisch in books mit angepasst.
    ON UPDATE CASCADE
-- Speicher-Engine InnoDB verwenden (Voraussetzung für die obigen Fremdschlüssel).
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabelle `borrowers`
-- -----------------------------------------------------

-- Tabelle "borrowers" anlegen, falls sie noch nicht existiert. Sie speichert die Stammdaten der Entleiher.
CREATE TABLE IF NOT EXISTS `mydb`.`borrowers` (
  -- Eindeutige, automatisch hochzählende ID des Entleihers (Primärschlüssel).
  `borrowerID` INT NOT NULL AUTO_INCREMENT,
  -- Vorname des Entleihers; Pflichtfeld.
  `first_name` VARCHAR(45) NOT NULL,
  -- Nachname des Entleihers; Pflichtfeld.
  `last_name` VARCHAR(60) NOT NULL,
  -- E-Mail-Adresse des Entleihers; optional.
  `email` VARCHAR(45) NULL,
  -- Telefonnummer des Entleihers; optional.
  `telephone` VARCHAR(22) NULL,
  -- Neu übernommen aus dem Schulskript: maximale Anzahl gleichzeitiger Ausleihen für diesen Entleiher,
  -- Standardwert 3, falls beim Anlegen kein individueller Wert angegeben wird.
  `max_loans` TINYINT DEFAULT 3,
  -- Neu übernommen aus dem Schulskript: Freitextfeld für Bemerkungen zum Entleiher (z. B. Besonderheiten).
  `borrower_notes` TEXT NULL,
  -- borrowerID als Primärschlüssel der Tabelle festlegen.
  PRIMARY KEY (`borrowerID`)
-- Speicher-Engine InnoDB verwenden.
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabelle `loans`
-- -----------------------------------------------------

-- Tabelle "loans" anlegen, falls sie noch nicht existiert. Sie protokolliert jeden Ausleihvorgang
-- und löst dadurch die n:m-Beziehung zwischen books und borrowers auf.
CREATE TABLE IF NOT EXISTS `mydb`.`loans` (
  -- Eindeutige, automatisch hochzählende ID der Ausleihe (Primärschlüssel).
  `loan_id` INT NOT NULL AUTO_INCREMENT,
  -- Verweis auf das ausgeliehene Buch (Fremdschlüssel zu books.bookID); Pflichtfeld.
  `bookID` INT NOT NULL,
  -- Verweis auf den Entleiher (Fremdschlüssel zu borrowers.borrowerID); Pflichtfeld.
  `borrowerID` INT NOT NULL,
  -- Übernommen aus dem Schulskript: Ausleihdatum, das automatisch auf das aktuelle Datum gesetzt wird,
  -- falls beim Einfügen kein Wert übergeben wird. Pflichtfeld.
  `loan_date` DATE DEFAULT (CURRENT_DATE()) NOT NULL,
  -- Neu übernommen aus dem Schulskript: Fälligkeitsdatum, automatisch 30 Tage nach dem Ausleihdatum.
  `due_date` DATE DEFAULT (DATE_ADD(loan_date, INTERVAL 30 DAY)),
  -- Datum der Rückgabe; optional, bleibt NULL solange das Buch nicht zurückgegeben wurde.
  `return_date` DATE NULL,
  -- Neu übernommen aus dem Schulskript: aussagekräftiger Status als Text (z. B. "ausgeliehen",
  -- "zurückgegeben", "überfällig") statt eines reinen 0/1-Flags; Pflichtfeld.
  `loan_status` VARCHAR(20) NOT NULL,
  -- loan_id als Primärschlüssel der Tabelle festlegen.
  PRIMARY KEY (`loan_id`),
  -- Index auf bookID anlegen, um Joins/Lookups über den Fremdschlüssel zu beschleunigen.
  INDEX `fk_loans_books1_idx` (`bookID` ASC) VISIBLE,
  -- Index auf borrowerID anlegen, um Joins/Lookups über den Fremdschlüssel zu beschleunigen.
  INDEX `fk_loans_borrowers1_idx` (`borrowerID` ASC) VISIBLE,
  -- Fremdschlüssel-Constraint: bookID muss auf einen existierenden Eintrag in books.bookID verweisen.
  CONSTRAINT `fk_loans_books1`
    FOREIGN KEY (`bookID`)
    REFERENCES `mydb`.`books` (`bookID`)
    -- Übernommen aus dem Schulskript: Wird ein Buch gelöscht, sollen auch seine Ausleihhistorie-Einträge
    -- automatisch mitgelöscht werden.
    ON DELETE CASCADE
    -- Ändert sich die bookID, wird sie automatisch in loans mit angepasst.
    ON UPDATE CASCADE,
  -- Fremdschlüssel-Constraint: borrowerID muss auf einen existierenden Eintrag in borrowers.borrowerID verweisen.
  CONSTRAINT `fk_loans_borrowers1`
    FOREIGN KEY (`borrowerID`)
    REFERENCES `mydb`.`borrowers` (`borrowerID`)
    -- Übernommen aus dem Schulskript: Ein Entleiher mit bestehenden Ausleih-Einträgen darf nicht gelöscht
    -- werden (Löschung wird verhindert), damit die Ausleihhistorie nicht verwaist.
    ON DELETE RESTRICT
    -- Beim Ändern der borrowerID keine automatische Aktion auslösen.
    ON UPDATE NO ACTION
-- Speicher-Engine InnoDB verwenden (Voraussetzung für die obigen Fremdschlüssel).
) ENGINE = InnoDB;


-- Ursprünglichen SQL_MODE aus der Session-Variable wiederherstellen.
SET SQL_MODE=@OLD_SQL_MODE;
-- Ursprünglichen Wert von FOREIGN_KEY_CHECKS wiederherstellen (Prüfungen wieder aktivieren).
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
-- Ursprünglichen Wert von UNIQUE_CHECKS wiederherstellen (Prüfungen wieder aktivieren).
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
