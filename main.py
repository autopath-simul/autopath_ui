# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.mainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    win = MainWindow(engine=None, job_manager=None)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()