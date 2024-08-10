import os
import sys
import time
import subprocess
from tkinter import Tk, Label, Button, W, E

def exit_download():
    os._exit(0)

def install_packages(packages):
    """Устанавливает пакеты с помощью pip и выводит сообщения."""

    global label  # Делаем label глобальной переменной
    start_time = time.time()

    for package in packages:
        print(f"Установка пакета: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        root.update_idletasks()
        label.config(text=f"Установка пакета: {package}\n")

    end_time = time.time()
    elapsed_time = end_time - start_time

    root.update_idletasks()
    label.config(text=f"Установка завершена!\nЗатраченное время: {elapsed_time:.2f} секунд\nВы можете закрыть это окно")
    button.config(text=f"Готово", command=exit_download())

if __name__ == '__main__':
    # Создаем главное окно Tkinter
    root = Tk()
    root.title("Установка пакетов")

    # Определяем список пакетов
    packages = ["PyQt5", "PyQtWebEngine"]

    # Текстовое поле для отображения процесса
    label = Label(root, text="Нажмите 'Установить',\nчтобы начать установку важных пакетов для работы CTube.", wraplength=300, justify="left")
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W + E)

    # Кнопка "Установить"
    def install_button_click():
        global button  # Делаем button глобальной переменной
        button.pack_forget()  # Скрываем кнопку
        install_packages(packages)

    button = Button(root, text="Установить", command=install_button_click)
    button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()