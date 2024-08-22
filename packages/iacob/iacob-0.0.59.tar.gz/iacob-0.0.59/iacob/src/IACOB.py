import os
import sys
from pathlib import Path


from PyQt5 import QtGui, QtWidgets 
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

QtGui.QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QtGui.QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

sys.path.append(str(Path(__file__).parent.parent))
from src.View.MainWindow_View import MainWindowView

import pyqtgraph as pg

def run_app():

    pg.setConfigOptions(antialias=True)

    version = "0.0.3"
    release_date = "2024-07-18"

    start_message = f"""
--------------------------------------------------------------
pyIACOB v{version} : {release_date}

Authors :
- frederic.andersson@univ-tours.fr
- enzo.creuzet@univ-tours.fr
- thibaud.scribe@univ-tours.fr
--------------------------------------------------------------
    """

    print(start_message)

    # -------------- Start ---------------

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("IACOB")

    mainwindow = MainWindowView()
    mainwindow.showMaximized()
    mainwindow.setWindowTitle("IACOB Application")

    # Load and apply the QSS file
    resources_dir = Path(__file__).parent.parent / 'resources'
    imagePath = os.path.join(resources_dir, "images", "chat_pixel.jpg")
    mainwindow.setWindowIcon(QIcon(imagePath))

    with open(os.path.join(resources_dir, "Style_Application.qss"), 'r') as file:
        stylesheet = file.read()
        app.setStyleSheet(stylesheet)
        app.setFont(QFont("Arial", 10))

    
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
