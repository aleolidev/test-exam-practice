from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog
from PyQt5.QtCore import QSettings

from frontend.central_widget import CentralWidget
from frontend.main_tests import ModeSelector

class MainWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Exam Practice")
        self.setFixedSize(270, 110)
        self.load_gui()
        self.connect_signals()

    def load_gui(self):
        self.menu_bar = self.menuBar()
        # ACTIONS!
        self.load_dataset = QAction("&Load Dataset", self)
        self.exit_action = QAction("&Exit", self)
        
        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("See information about this tool.")
        
        # MENUS!
        self.file_menu = self.menu_bar.addMenu("&File")
        self.file_menu.addActions([
            self.load_dataset,
            self.file_menu.addSeparator(),
            self.exit_action
        ])
        self.help_menu = self.menu_bar.addMenu("&Help")
        self.help_menu.addActions([
            self.about_action
        ])
        # SHORTCUTS!
        self.load_dataset.setShortcut("Ctrl+O")
        self.exit_action.setShortcut("Ctrl+Q")
        
        self.setMenuBar(self.menu_bar)
        
        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)
    
    def connect_signals(self):
        self.load_dataset.triggered.connect(lambda: self.add_dataset_options())

    def add_dataset_options(self):
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        self.file, _ = QFileDialog.getOpenFileName(self, 'Open file', self.settings.value("dataset"), '*.json')
        if self.file and self.file.endswith(".json"):
            self.settings.setValue("dataset", self.file)
            self.sprite_editor_tab = ModeSelector(self.file)
            self.central_widget.lay.addWidget(self.sprite_editor_tab)