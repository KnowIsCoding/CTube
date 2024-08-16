import sys  # Sys ist am Start, klar!
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QCheckBox, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QFrame, QSpacerItem, QSizePolicy, QToolButton, QListWidget, QListWidgetItem, QMenu, QSizePolicy, QApplication, QTabWidget, QSplitter, QFrame, QDesktopWidget, QPushButton, QLabel)  # PyQt5 Imports, voll die Power!
from PyQt5.QtGui import QFont, QIcon, QPixmap  # Fonts, Icons und Bilder importieren, alles am Start!
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QUrl, QTimer, QThread, pyqtSignal  # Core-Funktionen, damit läuft’s wie geschmiert!
import json  # JSON für die Konfig!
import string  # Strings für den Text
import random  # Zufall für den Spaß
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile  # Web-Engine-Widgets, für den Webkram
from PyQt5.QtNetwork import QNetworkProxy, QNetworkProxyFactory  # Netzwerk-Proxy, weil ohne geht's nicht!
import os  # OS für System-Interaktionen
import time  # Zeitfunktionen für Pausen
import webbrowser  # Browser für Webseiten
import requests  # Requests für HTTP-Anfragen
from bs4 import BeautifulSoup  # BeautifulSoup zum Schürfen von Daten

class A(QWidget):  # Klasse A, die GUI am Start!
    def __init__(self):  # Konstruktor, immer willkommen!
        super().__init__()  # Superklasse initialisieren, wie’s sich gehört!
        self.setWindowTitle("CTube")  # Fenster-Titel setzen, cool und klar
        self.setWindowIcon(QIcon("icons\\icon.png"))  # Fenster-Icon setzen, damit’s schick aussieht
        self.setStyleSheet("""  # Stylesheet definieren, für den Look
            QWidget {
                background-color: #222;  # Hintergrundfarbe, sieht edel aus
                color: #eee;  # Textfarbe, schick im Kontrast
                font-family: "Segoe UI", sans-serif;  # Schriftart setzen, damit’s professionell wirkt
            }
            QPushButton {
                background-color: #333;  # Hintergrundfarbe für Buttons, cool und edel
                color: #eee;  # Textfarbe für Buttons, damit man alles lesen kann
                border: 1px solid #555;  # Rahmen für Buttons, damit die Form klar ist
                border-radius: 5px;  # Abgerundete Ecken für den Button-Look
                padding: 5px 10px;  # Padding für den Button, damit er nicht so eng ist
            }
            QPushButton:hover {
                background-color: #444;  # Hover-Effekt für Buttons, damit man was sieht, wenn man drüber fährt
            }
            QLabel {
                background-color: #333;  # Hintergrundfarbe für Labels, passend zu Buttons
                padding: 5px;  # Padding für Labels, damit der Text nicht an den Rändern klebt
                border-radius: 5px;  # Abgerundete Ecken für Labels
            }
            #proxyLabel, #sessionLabel {
                background-color: #333;  # Hintergrundfarbe für spezielle Labels
                padding: 5px 10px;  # Padding für Labels, damit der Text gut aussieht
                border-radius: 5px;  # Abgerundete Ecken für den coolen Look
                color: #eee;  # Textfarbe für Labels, damit man alles lesen kann
            }
            #proxyButton {
                border: none;  # Kein Rahmen für diesen speziellen Button
                background-color: rgba(0, 0, 0, 0);  # Transparent für den speziellen Button
                border-radius: 5px;  # Abgerundete Ecken, damit es stilvoll aussieht
            }
            QTabWidget::tab-bar::tab:selected {
                border-bottom: 2px solid #444;  # Untere Rahmenlinie für ausgewählte Tabs
                border-bottom-left-radius: 0px;  # Keine abgerundeten Ecken unten links
                border-bottom-right-radius: 0px;  # Keine abgerundeten Ecken unten rechts
            }
            QTabWidget::tab-bar::tab:hover {
                border-bottom: 2px solid #555;  # Untere Rahmenlinie bei Hover über Tabs
                border-bottom-left-radius: 0px;  # Keine abgerundeten Ecken unten links
                border-bottom-right-radius: 0px;  # Keine abgerundeten Ecken unten rechts
            }
            QFrame[frameShape="HLine"] {
                background-color: #555;  # Farbe für horizontale Linien
                height: 1px;  # Höhe der Linie
                margin: 5px 0;  # Margin für Abstand oben und unten
            }
            #githubButton, #discordButton {
                background-color: #333;  # Hintergrundfarbe für spezielle Buttons
                color: #eee;  # Textfarbe für Buttons
                border: none;  # Kein Rahmen für diese Buttons
                padding: 0;  # Kein Padding für den cleanen Look
            }
            #githubButton:hover, #discordButton:hover {
                background-color: #444;  # Hover-Effekt für die Buttons
            }
            #githubButton::icon, #discordButton::icon {
                width: 24px;  # Breite der Icons
                height: 24px;  # Höhe der Icons
            }
        """)
        self.b = self.load_c()  # Einstellungen laden
        self.setWindowIcon(QIcon("icons\\icon.png"))  # Icon setzen, falls noch nicht geschehen
        self.d = QLabel("Prowxis:", self)  # Label für Proxies
        self.e = QCheckBox(self)  # Checkbox für Proxy-Status
        self.e.setChecked(self.b['proxy_status'])  # Checkbox initialisieren
        self.f = QLabel("Proxy Typ:", self)  # Label für Proxy-Typ
        self.g = QComboBox(self)  # Kombinationsfeld für Proxy-Typen
        self.g.addItems(["Eigene", "Integrierter Parser"])  # Proxy-Typen hinzufügen
        self.g.setCurrentText(self.b['proxy_type'])  # Aktuellen Proxy-Typ setzen
        self.h = QLabel("Website:", self)  # Label für Website
        self.i = QLineEdit(self)  # Textfeld für Website
        self.i.setText(self.b['website'])  # Textfeld initialisieren
        self.d.setFont(QFont("Segoe UI", 10, QFont.Bold))  # Schriftart für das Label setzen
        self.f.setFont(QFont("Segoe UI", 10, QFont.Bold))  # Schriftart für das Label setzen
        self.h.setFont(QFont("Segoe UI", 10, QFont.Bold))  # Schriftart für das Label setzen
        self.j = QLabel("Geladene Proxys:", self)  # Label für geladene Proxys
        self.j.setFont(QFont("Segoe UI", 10, QFont.Bold))  # Schriftart für das Label setzen
        self.k = self.load_d()  # Geladene Proxys abrufen
        self.l = QListWidget(self)  # Liste für Proxys
        self.l.addItems(self.k)  # Proxys zur Liste hinzufügen
        self.l.setContextMenuPolicy(Qt.CustomContextMenu)  # Kontextmenü für die Liste aktivieren
        self.l.customContextMenuRequested.connect(self.m)  # Kontextmenü verbinden
        self.n = QLabel(f"Anzahl: {len(self.k)}", self)  # Label für Anzahl der Proxys
        self.n.setFont(QFont("Segoe UI", 10, QFont.Bold))  # Schriftart für das Label setzen
        self.o = QPushButton("Scrapen", self)  # Button zum Scrapen
        self.o.clicked.connect(self.p)  # Button-Click mit Scraping-Funktion verbinden
        self.q = QPushButton("SPEICHERN", self)  # Button zum Speichern
        self.r = QPushButton("STANDARD", self)  # Button zum Zurücksetzen auf Standard
        self.s = QPushButton("STARTEN", self)  # Button zum Starten
        self.t = QPushButton(self)  # Button für GitHub
        self.t.setObjectName("githubButton")  # Objektname setzen
        self.t.clicked.connect(lambda: webbrowser.open("https://github.com/your_github_link"))  # Klick öffnet GitHub-Link
        self.u = QPushButton(self)  # Button für Discord
        self.u.setObjectName("discordButton")  # Objektname setzen
        self.u.clicked.connect(lambda: webbrowser.open("https://discord.com/invite/your_discord_link"))  # Klick öffnet Discord-Link
        self.v = QPixmap("icons\\github.png").scaled(24, 24, Qt.KeepAspectRatio)  # GitHub-Icon laden und skalieren
        self.w = QPixmap("icons\\discord.png").scaled(24, 24, Qt.KeepAspectRatio)  # Discord-Icon laden und skalieren
        self.t.setIcon(QIcon(self.v))  # GitHub-Icon setzen
        self.u.setIcon(QIcon(self.w))  # Discord-Icon setzen
        self.x = QFrame(self)  # Frame für Layout
        self.x.setFrameShape(QFrame.HLine)  # Frame als horizontale Linie
        self.y = QVBoxLayout(self)  # Layout für Widgets
        self.y.addWidget(self.d)  # Label hinzufügen
        self.y.addWidget(self.e)  # Checkbox hinzufügen
        self.y.addWidget(self.f)  # Label hinzufügen
        self.y.addWidget(self.g)  # Kombinationsfeld hinzufügen
        self.y.addWidget(self.h)  # Label hinzufügen
        self.y.addWidget(self.i)  # Textfeld hinzufügen
        self.y.addWidget(self.j)  # Label hinzufügen
        self.y.addWidget(self.l)  # Liste hinzufügen
        self.y.addWidget(self.n)  # Label hinzufügen
        self.y.addWidget(self.x)  # Rahmen hinzufügen
        self.y.addWidget(self.o)  # Scrape-Button hinzufügen
        self.y.addWidget(self.q)  # Speicher-Button hinzufügen
        self.y.addWidget(self.r)  # Standard-Button hinzufügen
        self.y.addWidget(self.s)  # Start-Button hinzufügen
        self.y.addWidget(self.t)  # GitHub-Button hinzufügen
        self.y.addWidget(self.u)  # Discord-Button hinzufügen
        self.setLayout(self.y)  # Layout setzen

    def load_c(self):  # Konfiguration laden
        try:  # Fehlerbehandlung
            with open("config.json", "r") as file:  # JSON-Datei öffnen
                return json.load(file)  # JSON laden
        except Exception as e:  # Fehler
            print(f"Fehler beim Laden der Konfigurationsdatei: {e}")  # Fehler ausgeben
            return {"proxy_status": False, "proxy_type": "Eigene", "website": ""}  # Standardwerte zurückgeben

    def load_d(self):  # Geladene Proxys
        try:  # Fehlerbehandlung
            with open("proxies.txt", "r") as file:  # Proxies-Datei öffnen
                return file.read().splitlines()  # Proxys einlesen
        except Exception as e:  # Fehler
            print(f"Fehler beim Laden der Proxys: {e}")  # Fehler ausgeben
            return []  # Leere Liste zurückgeben

    def m(self, pos):  # Kontextmenü öffnen
        menu = QMenu(self)  # Menü erstellen
        remove_action = menu.addAction("Entfernen")  # "Entfernen"-Option hinzufügen
        action = menu.exec_(self.l.mapToGlobal(pos))  # Menü anzeigen
        if action == remove_action:  # Wenn Entfernen ausgewählt
            for item in self.l.selectedItems():  # Für alle ausgewählten Items
                self.l.takeItem(self.l.row(item))  # Item entfernen
            self.n.setText(f"Anzahl: {len(self.k)}")  # Anzahl aktualisieren

    def p(self):  # Scrape-Funktion
        proxy_status = self.e.isChecked()  # Proxy-Status prüfen
        proxy_type = self.g.currentText()  # Proxy-Typ prüfen
        website = self.i.text()  # Website prüfen
        print(f"Proxy Status: {proxy_status}, Proxy Typ: {proxy_type}, Website: {website}")  # Ausgabe der Werte
        # Implementierung für Scraping geht hier hin

    def run(self):  # Anwendung starten
        self.show()  # Fenster anzeigen
        sys.exit(app.exec_())  # Anwendung ausführen und beenden

if __name__ == '__main__':  # Wenn das Skript direkt ausgeführt wird
    app = QApplication(sys.argv)  # Anwendung erstellen
    window = A()  # Fenster erstellen
    window.run()  # Fenster ausführen
