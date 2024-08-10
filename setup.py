import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
import json
import os
import subprocess
import requests

# Параметры
repo_url = "https://github.com/KnowIsCoding/CTube"
branch = "main"
local_filepath = "VERSION.JSON"
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patched_folder")  # Папка "patched_folder" в том же каталоге, что и скрипт

# Создать папку, если она не существует
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def get_github_version():
    """Получает версию из файла VERSION.JSON на GitHub."""
    url = f"https://raw.githubusercontent.com/KnowIsCoding/CTube/main/VERSION.JSON"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data['version']
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(None, "Ошибка", f"Не удалось получить версию с GitHub: {e}")
        return None

def get_local_version():
    """Получает версию из файла VERSION.JSON локально."""
    try:
        with open(local_filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        QMessageBox.critical(None, "Ошибка", "Файл VERSION.JSON не найден")
        return None

def compare_versions(github_version, local_version):
    """Сравнивает версии из GitHub и локально."""
    if github_version is None or local_version is None:
        return "Ошибка получения версии"

    if github_version != local_version['version']:
        return "Версии отличаются: GitHub: {}, Local: {}".format(github_version, local_version['version'])
    else:
        return "Версии совпадают: {}".format(github_version)

def update_folder():
    """Удаляет содержимое папки и скачивает новый контент."""
    try:
        # Удаление содержимого папки
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        
        # Скачивание нового контента
        command = f"git clone -b {branch} {repo_url} {folder_path}"
        subprocess.run(command, shell=True, check=True)
        
        QMessageBox.information(None, "Обновление", "Папка успешно обновлена!")
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Ошибка обновления папки: {e}")

def install_dependencies(dependencies):
    """Устанавливает зависимости из VERSION.JSON."""
    for dependency in dependencies:
        try:
            command = f"pip install {dependency}"
            subprocess.run(command, shell=True, check=True)
            print(f"Установка {dependency} завершена")
        except subprocess.CalledProcessError:
            QMessageBox.critical(None, "Ошибка", f"Ошибка установки {dependency}")
            break

def check_update():
    """Проверяет обновления и обновляет папку, если необходимо."""
    github_version = get_github_version()
    local_version = get_local_version()

    result = compare_versions(github_version, local_version)
    result_label.setText(result)

    if "отличаются" in result:
        if QMessageBox.question(None, "Обновление", "Обновить папку?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            update_folder()
            if local_version and 'dependencies' in local_version:
                install_dependencies(local_version['dependencies'])

# Tkinter
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка обновлений")
        self.initUI()

    def initUI(self):
        global result_label
        result_label = QLabel()
        self.check_button = QPushButton("Проверить обновления")
        self.check_button.clicked.connect(self.check_update)

        layout = QVBoxLayout()
        layout.addWidget(result_label)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def check_update(self):
        github_version = get_github_version()
        local_version = get_local_version()

        result = compare_versions(github_version, local_version)
        result_label.setText(result)

        if "отличаются" in result:
            if QMessageBox.question(None, "Обновление", "Обновить папку?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                update_folder()
                if local_version and 'dependencies' in local_version:
                    install_dependencies(local_version['dependencies'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())