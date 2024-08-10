import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ErrorWindow(QWidget):
    def __init__(self, error_name, error_description, discord_link):
        super().__init__()

        self.setWindowTitle("Ошибка")
        self.setStyleSheet("background-color: black;")

        # Создание надписи для имени ошибки
        self.error_name_label = QLabel(error_name)
        self.error_name_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.error_name_label.setAlignment(Qt.AlignCenter)

        # Создание надписи для описания ошибки
        self.error_description_label = QLabel(error_description)
        self.error_description_label.setFont(QFont("Arial", 10))
        self.error_description_label.setAlignment(Qt.AlignCenter)

        # Создание кнопки "OK"
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)

        # Создание кнопки "Перейти на сервер поддержки"
        self.support_button = QPushButton("Перейти на сервер поддержки")
        self.support_button.setFont(QFont("Arial", 8))
        self.support_button.clicked.connect(lambda: self.open_link(discord_link))

        # Создание вертикального макета
        layout = QVBoxLayout()
        layout.addWidget(self.error_name_label)
        layout.addWidget(self.error_description_label)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.support_button)
        self.setLayout(layout)

    def open_link(self, link):
        import webbrowser
        webbrowser.open_new_tab(link)