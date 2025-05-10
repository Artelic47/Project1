import sys
from PyQt6.QtWidgets import QApplication
from gui import TVRemoteApp

def main():
    app = QApplication(sys.argv)
    window = TVRemoteApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
