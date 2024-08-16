import sys  # Holen wir uns das sys-Modul für Systemkram
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox)  # PyQt5 Widgets am Start
from PyQt5.QtCore import Qt  # Qt für die Grundfunktionen
import json  # json-Modul für die JSON-Daten
import os  # os-Modul für die Dateikram
import subprocess  # subprocess für die Prozesserstellung
import requests  # requests für HTTP-Anfragen

a = "https://github.com/KnowIsCoding/CTube"  # GitHub-Repo-URL
b = "main"  # Branch-Name, der Hauptzweig
c = "VERSION.JSON"  # Dateiname für die Version
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gepatchter_ordner")  # Pfad zum Zielordner
if not os.path.exists(d):  # Checken, ob der Ordner noch nicht da ist
    os.makedirs(d)  # Machen wir den Ordner klar

def x():  # Funktion zum Versionen abholen von GitHub
    e = f"https://raw.githubusercontent.com/KnowIsCoding/CTube/main/VERSION.JSON"  # URL für die GitHub-Version
    try:  # Versuch macht klug
        f = requests.get(e)  # Anfrage an GitHub senden
        f.raise_for_status()  # Fehler checken, ob die Anfrage geklappt hat
        g = f.json()  # JSON-Daten rausholen
        return g['version']  # Version zurückgeben
    except requests.exceptions.RequestException as h:  # Wenn was schiefgeht
        QMessageBox.critical(None, "Fehler", f"Fehler beim Abrufen der Version von GitHub: {h}")  # Fehler melden
        return None  # Nix zurückgeben

def y():  # Funktion zum Abholen der lokalen Version
    try:  # Wieder ein Versuch
        i = open(c, "r")  # Die Version-Datei aufmachen
        j = json.load(i)  # JSON-Daten laden
        return j  # Lokale Version zurückgeben
    except FileNotFoundError:  # Wenn die Datei nicht gefunden wird
        QMessageBox.critical(None, "Fehler", "VERSION.JSON-Datei nicht gefunden")  # Fehlermeldung rausknallen
        return None  # Nix zurückgeben

def z(m, n):  # Funktion zum Vergleichen der Versionen
    if m is None or n is None:  # Checken ob eine der Versionen nicht da ist
        return "Fehler beim Vergleichen der Versionen"  # Fehlernachricht ausgeben
    if m != n['version']:  # Wenn Versionen nicht übereinstimmen
        return f"Versionen unterscheiden sich: GitHub: {m}, Lokal: {n['version']}"  # Unterschiedliche Versionen melden
    else:  # Wenn Versionen übereinstimmen
        return f"Versionen stimmen überein: {m}"  # Übereinstimmende Versionen melden

def w():  # Funktion zum Aufräumen des lokalen Ordners
    try:  # Noch ein Versuch
        for o in os.listdir(d):  # Durch die Sachen im Zielordner gehen
            p = os.path.join(d, o)  # Vollständigen Pfad bauen
            if os.path.isfile(p):  # Wenn es eine Datei ist
                os.remove(p)  # Datei löschen
            elif os.path.isdir(p):  # Wenn es ein Verzeichnis ist
                os.rmdir(p)  # Verzeichnis entfernen
    except Exception as q:  # Wenn irgendwas schiefgeht
        QMessageBox.critical(None, "Fehler", f"Fehler beim Aktualisieren des lokalen Ordners: {q}")  # Fehlermeldung ausgeben

def r():  # Funktion für mit Zufallszeug
    print("Wird hier zufälliger ausgeführt...")  # Zufällige Nachricht
    for s in range(10):  # Schleife von 0 bis 9
        print(f"Zufällige Zahl: {s}")  # Zufallszahl ausgeben
        if s % 2 == 0:  # Wenn Zahl gerade ist
            print("Gerade Zahl!")  # Nachricht für gerade Zahl
        else:  # Wenn Zahl ungerade ist
            print("Ungerade Zahl!")  # Nachricht für ungerade Zahl
    import math  # math-Modul für die Mathematik
    print(f"Die Quadratwurzel von 16 ist {math.sqrt(16)}")  # Quadratwurzel von 16 ausgeben
    print("Noch mehr hier.")  # Noch eine zufällige Nachricht
    import time  # time-Modul für Zeitzeug
    time.sleep(1)  # Eine Sekunde warten
    print("Pause beendet.")  # Nachricht nach der Pause
    a = [1, 2, 3, 4, 5]  # Liste erstellen
    b = [x * 2 for x in a]  # Liste verdoppeln
    print(f"Verdoppelte Liste: {b}")  # Verdoppelte Liste ausgeben
    c = {"Schlüssel": "Wert"}  # Dictionary erstellen
    print(f"Dictionary-Inhalt: {c}")  # Dictionary-Inhalt ausgeben
    for key, value in c.items():  # Durch Dictionary-Items gehen
        print(f"Schlüssel: {key}, Wert: {value}")  # Schlüssel und Wert ausgeben

if __name__ == "__main__":  # Wenn das Skript direkt gestartet wird
    app = QApplication(sys.argv)  # QApplication-Instanz erstellen
    window = QWidget()  # Hauptfenster erstellen
    layout = QVBoxLayout()  # Layout für das Fenster erstellen

    label = QLabel("Willkommen zu meiner App!")  # Beschriftung erstellen
    button = QPushButton("Klick mich!")  # Button erstellen
    
    def click_handler():  # Funktion für Button-Klicks
        v = x()  # GitHub-Version abholen
        l = y()  # Lokale Version abholen
        result = z(v, l)  # Versionen vergleichen
        QMessageBox.information(None, "Version Vergleich", result)  # Ergebnis anzeigen
    
    button.clicked.connect(click_handler)  # Klick-Handler an den Button binden
    
    layout.addWidget(label)  # Beschriftung zum Layout hinzufügen
    layout.addWidget(button)  # Button zum Layout hinzufügen
    window.setLayout(layout)  # Layout für das Fenster setzen
    window.show()  # Fenster anzeigen
    sys.exit(app.exec_())  # Anwendung ausführen und beenden
