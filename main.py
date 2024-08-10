import sys
from CTube import MainWindow
from PyQt5.QtWidgets import QApplication

# print("Pizdec a ne kod esli chestno :(")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())