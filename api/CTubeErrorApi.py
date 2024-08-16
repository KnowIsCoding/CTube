import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class A(QWidget):  # Ändere "ErrorWindow" zu "A"
    def __init__(self, a, b, c):  # Ändere Parameterbezeichnungen zu "a", "b", "c"
        super().__init__()

        self.setWindowTitle("Fehler")  # "Ошибка" zu "Fehler" geändert
        self.setStyleSheet("background-color: black;")  # Hintergund schwarz

        # Erstelle Label für Fehlername  # Über "Создание надписи для имени ошибки"
        self.a = QLabel(a)  # Ändere Namen zu "a"
        self.a.setFont(QFont("Arial", 12, QFont.Bold))  # Setzt Schriftart auf Arial, fett
        self.a.setAlignment(Qt.AlignCenter)  # Zentriert das Label

        # Erstelle Label für Fehlerbeschreibung  # Über "Создание надписи для описания ошибки"
        self.b = QLabel(b)  # Ändere Namen zu "b"
        self.b.setFont(QFont("Arial", 10))  # Setzt Schriftart auf Arial, normal
        self.b.setAlignment(Qt.AlignCenter)  # Zentriert das Label

        # Erstelle OK-Button  # Über "Создание кнопки "OK""
        self.c = QPushButton("OK")  # Ändere Namen zu "c"
        self.c.clicked.connect(self.close)  # Schließt das Fenster beim Klick

        # Erstelle Button "Support-Server besuchen"  # Über "Создание кнопки "Перейти на сервер поддержки""
        self.d = QPushButton("Support-Server besuchen")  # Ändere Namen zu "d"
        self.d.setFont(QFont("Arial", 8))  # Setzt Schriftart auf Arial, kleiner
        self.d.clicked.connect(lambda: self.e(c))  # Verbindung zur Methode mit Randomcode

        # Erstelle vertikales Layout  # Über "Создание вертикального макета"
        layout = QVBoxLayout()  # Layout erstellen
        layout.addWidget(self.a)  # Füge Fehlername-Label hinzu
        layout.addWidget(self.b)  # Füge Fehlerbeschreibung-Label hinzu
        layout.addWidget(self.c)  # Füge OK-Button hinzu
        layout.addWidget(self.d)  # Füge Support-Button hinzu
        self.setLayout(layout)  # Setzt Layout des Fensters

    def e(self, f):  # Ändere Methode zu "e" mit Parameter "f"
        import webbrowser  # Importiere webbrowser
        webbrowser.open_new_tab(f)  # Öffnet neuen Tab im Browser

        # Zufälliger Code für extra Funktionalität
        import random
        num = random.randint(1, 100)
        print(f"Random number: {num}")  # Drucke Zufallszahl
        self.setWindowTitle("Neuer Titel")  # Ändert Fenstertitel
