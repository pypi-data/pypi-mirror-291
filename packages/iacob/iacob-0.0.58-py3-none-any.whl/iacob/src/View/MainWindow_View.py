import os
from pathlib import Path

from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.Controller.MainWindow_Controller import MainWindow_Controller
from src.View.ui.MainWindow_ui import Ui_IACOB


class MainWindowView(QMainWindow, Ui_IACOB):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.openRecentProjects_menu = None
        self.openRecentFilters_menu = None

        self.mainWindow_controller = MainWindow_Controller(self)
        self.menuBar.setNativeMenuBar(False)

        self._InitView()
        self._InitActions()
        self._InitGraphPreparation()
        self._InitColorPaletteChoice()

    def _InitView(self):

        # Hide the dock widget for the "FileInfo" tab only
        if self.mainTabWidget.currentIndex() == 0:
            self.dockWidget.hide()
        else:
            self.dockWidget.show()

        # Tab1 : File Infos
        self.fileInfosSupport_Frame.hide()
        self.noInfoTab1_Label.show()

        # Tab2 : Circular
        self.circularTabSupport_Frame.hide()
        self.noInfoTab2_Label.show()

        # Tab3 : Pie
        self.pieTabWidget.hide()
        self.noInfoTab3_Label.show()

        # Tab4 : List
        self.listSupport_Frame.hide()
        self.noInfoTab4_Label.show()

        # Tab5 : GT
        self.tabGTWidget.hide()
        self.noInfoTab5_Label.show()

    # =======================================================
    # Method to create Figure and Canvas to display Histogram
    # =======================================================
    def _InitGraphPreparation(self):

        # Create a Matplotlib figure and a canvas to display it
        self.graph_curve = Figure()
        self.canvas = FigureCanvas(self.graph_curve)
        self.graphDisplay_Layout.addWidget(self.canvas)

        # Add two custom QLineEdit for discardWeight and discardAbsWeight inputs
    
    def _InitActions(self):

        # ===== Project / Filters Files ======

        # ----- Project Files -----

        # & define a quick key to jump to this menu by pressing alt+F
        self.file_toolBarMenu = self.menuBar.addMenu("&Files")
        self.file_toolBarMenu.addAction(self.mainWindow_controller.createProject_action)
        self.file_toolBarMenu.addAction(self.mainWindow_controller.openProject_action)

        # Open Recent Project
        self.openRecentProjects_menu = self.file_toolBarMenu.addMenu("Open Recent Project")

        self.separatorRecentProject = self.openRecentProjects_menu.addSeparator()
        self.openRecentProjects_menu.addAction(self.mainWindow_controller.clearRecentProjects_action)

        self.file_toolBarMenu.addAction(self.mainWindow_controller.exportProject_action)
        self.file_toolBarMenu.addAction(self.mainWindow_controller.closeProject_action)

        # ----- Filters Files -----
        self.separator = self.file_toolBarMenu.addSeparator()
        self.openFilters = self.file_toolBarMenu.addAction(self.mainWindow_controller.openFilters_action)

        # Open Recent Filters
        self.openRecentFilters = self.openRecentFilters_menu = self.file_toolBarMenu.addMenu("Open Recent Filters")

        self.separatorRecentFilters = self.openRecentFilters_menu.addSeparator()
        self.exportFilters = self.openRecentFilters_menu.addAction(self.mainWindow_controller.clearRecentFilters_action)

        self.file_toolBarMenu.addAction(self.mainWindow_controller.exportFilters_action)

        # ===== Other Buttons ======
        self.help_toolBarAction = self.menuBar.addAction(self.mainWindow_controller.help_action)
        self.about_toolBarAction = self.menuBar.addAction(self.mainWindow_controller.about_action)
        self.test_toolBarAction = self.menuBar.addAction(self.mainWindow_controller.test_action)

        self.resetFilter_button.setDefaultAction(self.mainWindow_controller.resetFilter_action)
        self.resetGraphicFilter_button.setDefaultAction(self.mainWindow_controller.resetGraphicFilter_action)
        self.exportCircular_button.setDefaultAction(self.mainWindow_controller.exportCircularGraphic_action)
        self.exportList_button.setDefaultAction(self.mainWindow_controller.exportList_action)

        self.mainWindow_controller._InitToolBar()

    def _InitColorPaletteChoice(self):

        colorPalettes = {
        "Red -> White -> Blue": [QColor(255, 0, 0), QColor(200, 200, 200), QColor(0, 0, 255)],
        "White -> Blue": [QColor(255, 255, 255), QColor(0, 0, 255)],
        "White -> Red": [QColor(255, 255, 255), QColor(255, 0, 0)],
        "White -> Brown": [QColor(255, 255, 255), QColor(165, 42, 42)],
        "Rainbow": [
            QColor(255, 0, 0),    # Red
            QColor(255, 165, 0),  # Orange
            QColor(255, 255, 0),  # Yellow
            QColor(0, 255, 0),    # Green
            QColor(0, 0, 255),    # Blue
            QColor(75, 0, 130),   # Indigo
            QColor(238, 130, 238) # Violet
            ]   
        }

        for palette_name, colors in colorPalettes.items():
            # Ajouter le texte et associer les couleurs comme data
            self.colorPalette_comboBox.addItem(palette_name, colors)

    def LoadIcon(self, iconType):

        resourcedir = Path(__file__).parent.parent.parent / 'resources'
        imagePath = os.path.join(resourcedir, "images", iconType + ".png")

        return QIcon(imagePath)
 
    def WarningPopUpFilters(self):

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Coherence Filters")
        msgBox.setText("Data, FLUT and Filters files are not coherent.\nDo you want ignore Incoherence(s) ?")
        msgBox.setWindowIcon(self.LoadIcon("warning"))

        ignoreButton = QPushButton("Ignore")
        cancelButton = QPushButton("Cancel")

        msgBox.addButton(ignoreButton, QMessageBox.ActionRole)
        msgBox.addButton(cancelButton, QMessageBox.ActionRole)

        ignoreButton.clicked.connect(self.mainWindow_controller.IgnoreFiltersIncoherences)
        cancelButton.clicked.connect(self.mainWindow_controller.CancelFilters)

        msgBox.exec_()

    def WarningPopUpNumberRegion(self):

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Region Number")
        msgBox.setText("The number of regions is higher than the recommended number (150 with blanks). \
                       \nDo you want to display all regions, or hide regions with 0 connexions ?")
        msgBox.setWindowIcon(self.LoadIcon("warning"))

        displayButton = QPushButton("Display")
        hideButton = QPushButton("Hide")

        msgBox.addButton(displayButton, QMessageBox.ActionRole)
        msgBox.addButton(hideButton, QMessageBox.ActionRole)

        displayButton.clicked.connect(self.mainWindow_controller.DisplayAllRegions)
        hideButton.clicked.connect(self.mainWindow_controller.HideRegions)

        msgBox.exec_() 
    
    def WarningPopUpValidation(self):

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Coherence Verification")
        msgBox.setText("Data and FLUT files are not coherent. \
                       \nDo you want ignore Incoherence(s) ?")
        msgBox.setWindowIcon(self.LoadIcon("warning"))

        ignoreButton = QPushButton("Ignore")
        cancelButton = QPushButton("Cancel")

        msgBox.addButton(ignoreButton, QMessageBox.ActionRole)
        msgBox.addButton(cancelButton, QMessageBox.ActionRole)

        ignoreButton.clicked.connect(self.mainWindow_controller.IgnoreValidationIncoherences)
        cancelButton.clicked.connect(self.mainWindow_controller.CancelValidation)

        msgBox.exec_()

    def ErrorLoading(self, text):

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Error Display")
        msgBox.setText(text)
        msgBox.setWindowIcon(self.LoadIcon("error"))

        okButton = QPushButton("OK")
        msgBox.addButton(okButton, QMessageBox.ActionRole)
        okButton.clicked.connect(msgBox.accept)

        msgBox.exec_()
    
    # =======================================
    # Method called when the window is closed
    # =======================================
    def closeEvent(self, event):

        # when the application is closed, called the control to save some data
        if hasattr(self, 'mainWindow_controller'):
            self.mainWindow_controller.SaveData()