import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QCheckBox, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QFrame, QSpacerItem, QSizePolicy, QToolButton, QListWidget, QListWidgetItem, QMenu, QSizePolicy, QApplication, QTabWidget, QSplitter, QFrame, QDesktopWidget, QPushButton, QLabel)
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QUrl, QTimer, QThread, pyqtSignal
import json
import string
import random
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtNetwork import QNetworkProxy, QNetworkProxyFactory
import os
import time
import webbrowser
import requests
from bs4 import BeautifulSoup

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CTube")
        self.setWindowIcon(QIcon("icons\\icon.png"))  # Замените "icons\\icon.png" на путь к вашей иконке

        self.setStyleSheet("""
            QWidget {
                background-color: #222;
                color: #eee;
                font-family: "Segoe UI", sans-serif;
            }
            QPushButton {
                background-color: #333;
                color: #eee;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QLabel {
                background-color: #333;
                padding: 5px;
                border-radius: 5px;
            }

            /* Дополнительные стили для информации */
            #proxyLabel, #sessionLabel {
                background-color: #333;
                padding: 5px 10px;
                border-radius: 5px;
                color: #eee;
            }
            #proxyButton {
                border: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 5px;
            }

            /* Переход между вкладками */
            QTabWidget::tab-bar::tab:selected {
                border-bottom: 2px solid #444;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QTabWidget::tab-bar::tab:hover {
                border-bottom: 2px solid #555;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            
            /* Разделители */
            QFrame[frameShape="HLine"] {
                background-color: #555;
                height: 1px;
                margin: 5px 0;
            }

            /* Кнопки GitHub и Discord */
            #githubButton, #discordButton {
                background-color: #333;
                color: #eee;
                border: none; /* Убираем рамку */
                padding: 0;  /* Убираем отступы */
            }
            #githubButton:hover, #discordButton:hover {
                background-color: #444;
            }

            /* Стили для иконок */
            #githubButton::icon, #discordButton::icon {
                width: 24px;
                height: 24px;
            }
        """)

        # Загрузка настроек
        self.load_settings()

        # Устанавливаем иконку после стилей
        self.setWindowIcon(QIcon("icons\\icon.png"))  # Замените "icons\\icon.png" на путь к вашей иконке

        # Создаем элементы
        self.proxy_label = QLabel("Проксилизация:", self)
        self.proxy_checkbox = QCheckBox(self)
        self.proxy_checkbox.setChecked(self.settings['proxy_enabled'])

        self.proxy_type_label = QLabel("Тип прокси:", self)
        self.proxy_type_combo = QComboBox(self)
        self.proxy_type_combo.addItems(["Свои", "Встроенный парсер"])
        self.proxy_type_combo.setCurrentText(self.settings['proxy_type'])

        self.site_label = QLabel("Сайт:", self)
        self.site_edit = QLineEdit(self)  # Теперь QLineEdit
        self.site_edit.setText(self.settings['site'])

        # Настраиваем шрифты
        self.proxy_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.proxy_type_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.site_label.setFont(QFont("Segoe UI", 10, QFont.Bold))

        # Загруженные прокси
        self.proxy_list_label = QLabel("Загруженные прокси:", self)
        self.proxy_list_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.proxy_list = self.load_proxies_from_folder()
        self.proxy_list_widget = QListWidget(self)
        self.proxy_list_widget.addItems(self.proxy_list)
        self.proxy_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.proxy_list_widget.customContextMenuRequested.connect(self.show_proxy_menu)

        self.proxy_count_label = QLabel(f"Количество: {len(self.proxy_list)}", self)
        self.proxy_count_label.setFont(QFont("Segoe UI", 10, QFont.Bold))

        # Кнопка "Спарсить"
        self.parse_button = QPushButton("Спарсить", self)
        self.parse_button.clicked.connect(self.parse_proxies_and_update_list)

        # Кнопки
        self.save_button = QPushButton("СОХРАНИТЬ", self)
        self.default_button = QPushButton("ПО УМОЛЧАНИЮ", self)
        self.launch_button = QPushButton("ЗАПУСТИТЬ", self)

        # Кнопки GitHub и Discord
        self.github_button = QPushButton(self)
        self.github_button.setObjectName("githubButton")
        self.github_button.clicked.connect(lambda: webbrowser.open("https://github.com/your_github_link"))  # Замените на ссылку на ваш GitHub

        self.discord_button = QPushButton(self)
        self.discord_button.setObjectName("discordButton")
        self.discord_button.clicked.connect(lambda: webbrowser.open("https://discord.com/invite/your_discord_link"))  # Замените на ссылку на ваш Discord

        # Загрузка изображений для кнопок
        self.github_pixmap = QPixmap("icons\\github.png").scaled(24, 24, Qt.KeepAspectRatio)  # Замените "icons\\github.png" на путь к картинке
        self.discord_pixmap = QPixmap("icons\\discord.png").scaled(24, 24, Qt.KeepAspectRatio)  # Замените "icons\\discord.png" на путь к картинке

        # Установка изображений для кнопок
        self.github_button.setIcon(QIcon(self.github_pixmap))
        self.discord_button.setIcon(QIcon(self.discord_pixmap))

        # Настраиваем компоновку
        main_layout = QVBoxLayout()

        # Настройки
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.proxy_label)
        settings_layout.addWidget(self.proxy_checkbox)
        settings_layout.addWidget(self.proxy_type_label)
        settings_layout.addWidget(self.proxy_type_combo)
        settings_layout.addWidget(self.site_label)
        settings_layout.addWidget(self.site_edit)
        settings_layout.addWidget(QFrame(self), alignment=Qt.AlignTop) # Разделитель
        settings_layout.addWidget(self.proxy_list_label)
        settings_layout.addWidget(self.proxy_list_widget)

        # Раздел с количеством прокси и кнопкой "Спарсить"
        proxy_count_layout = QHBoxLayout()
        proxy_count_layout.addWidget(self.proxy_count_label)
        proxy_count_layout.addWidget(self.parse_button)
        settings_layout.addLayout(proxy_count_layout)

        settings_layout.addWidget(QFrame(self), alignment=Qt.AlignTop) # Разделитель
        settings_layout.addWidget(QFrame(self), alignment=Qt.AlignTop) # Разделитель
        settings_layout.addWidget(QFrame(self), alignment=Qt.AlignTop) # Разделитель

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.default_button)
        button_layout.addWidget(self.launch_button)
        button_layout.addStretch()
        settings_layout.addLayout(button_layout)

        # Кнопки GitHub и Discord (в левом нижнем углу)
        github_discord_layout = QHBoxLayout()
        github_discord_layout.addWidget(self.github_button)
        github_discord_layout.addWidget(self.discord_button)
        settings_layout.addLayout(github_discord_layout)

        # Создаем QWidget для settings_layout
        settings_widget = QWidget()
        settings_widget.setLayout(settings_layout)

        # Загруженные прокси
        proxy_list_layout = QVBoxLayout()
        proxy_list_layout.addWidget(self.proxy_list_label)
        proxy_list_layout.addWidget(self.proxy_list_widget)
        proxy_list_layout.addWidget(self.proxy_count_label)

        proxy_list_widget = QWidget()
        proxy_list_widget.setLayout(proxy_list_layout)

        # Разделитель
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(settings_widget) # Теперь используем settings_widget
        splitter.addWidget(proxy_list_widget)
        splitter.setSizes([200, 150]) # Относительный размер левой и правой частей

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        # Центрируем окно
        self.center_window()

        # Подключаем обработчики событий
        self.proxy_checkbox.stateChanged.connect(self.on_proxy_changed)
        self.proxy_type_combo.currentIndexChanged.connect(self.on_proxy_type_changed)
        self.site_edit.textChanged.connect(self.on_site_changed)
        self.save_button.clicked.connect(self.save_settings)
        self.default_button.clicked.connect(self.load_default_settings)
        self.launch_button.clicked.connect(self.launch_web_view)

    def on_proxy_changed(self):
        self.settings['proxy_enabled'] = self.proxy_checkbox.isChecked()
        self.save_settings()

    def on_proxy_type_changed(self):
        self.settings['proxy_type'] = self.proxy_type_combo.currentText()
        self.save_settings()

    def on_site_changed(self):
        self.settings['site'] = self.site_edit.text()
        self.save_settings()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                'proxy_enabled': False,
                'proxy_type': 'Свои',
                'site': 'youtube'
            }

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

    def load_default_settings(self):
        self.settings = {
            'proxy_enabled': False,
            'proxy_type': 'Свои',
            'site': 'youtube.com'
        }
        self.proxy_checkbox.setChecked(False)
        self.proxy_type_combo.setCurrentText("Свои")
        self.site_edit.setText("youtube")
        self.save_settings()

    def launch_web_view(self):
        parsed_proxies = self.parse_proxies()
        if not parsed_proxies:
            self.parse_proxies_and_update_list()
            parsed_proxies = self.parse_proxies()  # Повторный парсинг, если список пуст

        self.web_view = WebView(self.settings, parsed_proxies)
        self.web_view.setWindowTitle(f"CTube - {self.settings['site']}")
        self.web_view.resize(800, 600)
        self.web_view.show()

    def load_proxies_from_folder(self):
        proxy_list = []
        proxies_folder = 'proxies'
        if os.path.isdir(proxies_folder):
            for filename in os.listdir(proxies_folder):
                if filename.endswith(".txt"):
                    with open(os.path.join(proxies_folder, filename), 'r') as f:
                        for line in f:
                            proxy_list.append(line.strip())
        return proxy_list
    def parse_proxies(self):
        proxy_list = []

        if self.settings['proxy_type'] == "Свои":
            # Загрузка прокси из файлов в папке 'proxies'
            proxies_folder = 'proxies'
            if os.path.isdir(proxies_folder):
                for proxy_filename in os.listdir(proxies_folder):
                    if proxy_filename.endswith(".txt"):
                        with open(os.path.join(proxies_folder, proxy_filename), 'r') as proxy_file:
                            for proxy in proxy_file:
                                proxy_list.append(proxy.strip())
            else:
                print(f"Папка с прокси '{proxies_folder}' не найдена.")

        else:
            # Загрузка прокси с сайтов
            sites_folder = 'sites'
            if os.path.isdir(sites_folder):
                for site_filename in os.listdir(sites_folder):
                    if site_filename.endswith(".txt"):
                        with open(os.path.join(sites_folder, site_filename), 'r') as site_file:
                            for site in site_file:
                                site = site.strip()

                                try:
                                    response = requests.get(site)
                                    response.raise_for_status()

                                    soup = BeautifulSoup(response.content, 'html.parser')
                                    proxies_text = soup.get_text() 

                                    for proxy in proxies_text.splitlines():
                                        proxy = proxy.strip() 
                                        if proxy:
                                            proxy_list.append(proxy)

                                except requests.exceptions.RequestException as e:
                                    print(f"Ошибка при скачивании сайта {site}: {e}")

            else:
                print(f"Папка с сайтами '{sites_folder}' не найдена.")

        # Сохранение прокси в файл (только если они получены с сайтов)
        if self.settings['proxy_type'] != "Свои" and proxy_list:
            filename = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + '.txt'
            filepath = os.path.join('proxies', filename)
            os.makedirs('proxies', exist_ok=True)

            with open(filepath, 'w') as f:
                for proxy in proxy_list:
                    f.write(proxy + '\n')

            print(f"Прокси сохранены в файл: {filepath}")
        elif self.settings['proxy_type'] == "Свои" and not proxy_list:
            print("Список прокси пуст.")

        return proxy_list

    def parse_proxies_and_update_list(self):
        """Парсит прокси и обновляет список прокси."""
        self.proxy_list = self.parse_proxies()  # Парсинг прокси
        self.proxy_list_widget.clear()  # Очищаем список
        self.proxy_list_widget.addItems(self.proxy_list)  # Добавляем новые прокси
        self.proxy_count_label.setText(f"Количество: {len(self.proxy_list)}")
        print("Спаршено по кнопке")

    def show_proxy_menu(self, point):
        menu = QMenu(self)
        remove_action = menu.addAction("Удалить прокси")
        action = menu.exec_(self.proxy_list_widget.mapToGlobal(point))
        if action == remove_action:
            selected_items = self.proxy_list_widget.selectedItems()
            if selected_items:
                for item in selected_items:
                    self.proxy_list.remove(item.text())
                    self.proxy_list_widget.takeItem(self.proxy_list_widget.row(item))
                self.proxy_count_label.setText(f"Количество: {len(self.proxy_list)}")

    def center_window(self):
        """Центрирует окно на экране."""
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def load_sites_from_file(self):
        sites = []
        assets_folder = "assets"
        sites_file = "sites.txt"
        if os.path.isdir(assets_folder) and os.path.isfile(os.path.join(assets_folder, sites_file)):
            with open(os.path.join(assets_folder, sites_file), 'r') as f:
                for line in f:
                    sites.append(line.strip())
        return sites
    
class WebView(QWidget):
    def __init__(self, settings=None, parsed_proxies=None):
        super().__init__()

        self.settings = settings
        self.proxy_list = parsed_proxies  # Используем список прокси из MainWindow
        self.current_proxy = None
        self.session_start_time = time.time()
        self.session_timer = QTimer()
        self.session_timer.timeout.connect(self.update_session_time)
        self.session_timer.start(1000)  # Обновлять время каждые 1 секунду

        # Создаем элементы управления
        self.proxy_button = QToolButton(self)
        self.proxy_button.setIcon(QIcon("icons/reload.png"))  # Замените "icons/refresh.png" на ваш путь к иконке
        self.proxy_button.clicked.connect(self.change_proxy)
        self.proxy_button.setStyleSheet("border: none; background-color: rgba(0, 0, 0, 0);")
        self.proxy_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.proxy_button.setFixedSize(QSize(25, 25))


        self.proxy_label = QLabel("Прокси: ---", self)
        self.proxy_label.setObjectName("proxyLabel")
        self.session_label = QLabel("Сессия: 00:00:00", self)
        self.session_label.setObjectName("sessionLabel")

        # Настраиваем шрифты
        self.proxy_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.session_label.setFont(QFont("Segoe UI", 10, QFont.Bold))

        # Создаем макет
        layout = QHBoxLayout()
        layout.addWidget(self.proxy_label)
        layout.addWidget(self.session_label)
        layout.addWidget(self.proxy_button, alignment=Qt.AlignRight)  # Переставили кнопку прокси
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем макет для WebView
        web_view_layout = QVBoxLayout()
        self.web_view = QWebEngineView(self)
        self.web_view.setStyleSheet("background-color: #181818; color: #eee;")  # Добавляем темный фон
        self.web_view.load(QUrl(f"https://{self.settings['site']}"))
        self.web_view.resize(600, 400)
        web_view_layout.addLayout(layout)
        web_view_layout.addWidget(self.web_view)
        self.setLayout(web_view_layout)

        self.reload_button = QToolButton(self)
        self.reload_button.setIcon(QIcon("icons/refresh.png"))  # Замените "icons/reload.png" на ваш путь к иконке
        self.reload_button.clicked.connect(self.web_view.reload)
        self.reload_button.setStyleSheet("border: none; background-color: rgba(0, 0, 0, 0);")
        self.reload_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.reload_button.setFixedSize(QSize(25, 25))

        layout.addWidget(self.reload_button, alignment=Qt.AlignRight)
        
        # Устанавливаем прокси при запуске
        self.set_proxy()

    def change_proxy(self):
        if self.proxy_list:
            self.current_proxy = self.proxy_list.pop(0)  # Берем следующий прокси
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.HttpProxy)
            proxy.setHostName(self.current_proxy.split(':')[0])
            proxy.setPort(int(self.current_proxy.split(':')[1]))
            QNetworkProxy.setApplicationProxy(proxy)
            self.proxy_label.setText(f"Прокси: {self.current_proxy}")
            self.setWindowTitle(f"CTube - {self.settings['site']} - Прокси: {self.current_proxy} - Сессия: 00:00:00")
            print(f"Сменили прокси на: {self.current_proxy}")
        else:
            print("Прокси-файлы не найдены в папке 'proxies'.")

    def set_proxy(self):
        if self.settings['proxy_enabled']:
            if self.settings['proxy_type'] == 'Свои':
                self.proxy_list = self.load_proxies_from_folder()
                if self.proxy_list:
                    self.current_proxy = self.proxy_list.pop(0)
                    proxy = QNetworkProxy()
                    proxy.setType(QNetworkProxy.HttpProxy)
                    proxy.setHostName(self.current_proxy.split(':')[0])
                    proxy.setPort(int(self.current_proxy.split(':')[1]))
                    QNetworkProxy.setApplicationProxy(proxy)
                    self.proxy_label.setText(f"Прокси: {self.current_proxy}")
                    self.setWindowTitle(f"CTube - {self.settings['site']} - Прокси: {self.current_proxy} - Сессия: 00:00:00")
                else:
                    self.parse_proxies()
                    print("Прокси-файлы не найдены в папке 'proxies'.")
                    print("Используем встроенный прокси-парсер.")
            else:
                print("Используем встроенный прокси-парсер.")
    def parse_proxies(self):
        proxy_list = []

        if self.settings['proxy_type'] == "Свои":
            # Загрузка прокси из файлов в папке 'proxies'
            proxies_folder = 'proxies'
            if os.path.isdir(proxies_folder):
                for proxy_filename in os.listdir(proxies_folder):
                    if proxy_filename.endswith(".txt"):
                        with open(os.path.join(proxies_folder, proxy_filename), 'r') as proxy_file:
                            for proxy in proxy_file:
                                proxy_list.append(proxy.strip())
            else:
                print(f"Папка с прокси '{proxies_folder}' не найдена.")

        else:
            # Загрузка прокси с сайтов
            sites_folder = 'sites'
            if os.path.isdir(sites_folder):
                for site_filename in os.listdir(sites_folder):
                    if site_filename.endswith(".txt"):
                        with open(os.path.join(sites_folder, site_filename), 'r') as site_file:
                            for site in site_file:
                                site = site.strip()

                                try:
                                    response = requests.get(site)
                                    response.raise_for_status()

                                    soup = BeautifulSoup(response.content, 'html.parser')
                                    proxies_text = soup.get_text() 

                                    for proxy in proxies_text.splitlines():
                                        proxy = proxy.strip() 
                                        if proxy:
                                            proxy_list.append(proxy)

                                except requests.exceptions.RequestException as e:
                                    print(f"Ошибка при скачивании сайта {site}: {e}")

            else:
                print(f"Папка с сайтами '{sites_folder}' не найдена.")

        # Сохранение прокси в файл (только если они получены с сайтов)
        if self.settings['proxy_type'] != "Свои" and proxy_list:
            filename = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + '.txt'
            filepath = os.path.join('proxies', filename)
            os.makedirs('proxies', exist_ok=True)

            with open(filepath, 'w') as f:
                for proxy in proxy_list:
                    f.write(proxy + '\n')

            print(f"Прокси сохранены в файл: {filepath}")
        elif self.settings['proxy_type'] == "Свои" and not proxy_list:
            print("Список прокси пуст.")

        return proxy_list
    
    def update_session_time(self):
        session_seconds = int(time.time() - self.session_start_time)
        minutes, seconds = divmod(session_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.session_label.setText(f"Сессия: {hours:02d}:{minutes:02d}:{seconds:02d}")
        self.setWindowTitle(f"CTube - {self.settings['site']} - Прокси: {self.current_proxy} - Сессия: {hours:02d}:{minutes:02d}:{seconds:02d}")

    def load_proxies_from_folder(self):
        proxy_list = []
        proxies_folder = 'proxies'
        if os.path.isdir(proxies_folder):
            for filename in os.listdir(proxies_folder):
                if filename.endswith(".txt"):
                    with open(os.path.join(proxies_folder, filename), 'r') as f:
                        for line in f:
                            proxy_list.append(line.strip())
        return proxy_list
