import os, sys
sys.path.append(os.path.dirname(__file__))

import sys
from PyQt5.QtWidgets import QApplication
from ui.mainWindow import MainWindow

from core.engine import SimulationEngine
from core.job import JobManager

def main():
    app = QApplication(sys.argv)
    engine = SimulationEngine()
    job_manager = JobManager()
    win = MainWindow(engine=engine, job_manager=job_manager)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
