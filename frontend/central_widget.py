from PyQt5.QtWidgets import QFileDialog, QWidget, QVBoxLayout
from PyQt5.QtCore import QSettings, QDir

from frontend.mode_selector import ModeSelector


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = 0
        self.load_gui()
        self.show()
    
    def load_gui(self):
        self.lay = QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay)

    def add_dataset_options(self):
        self.settings = QSettings("pyqt_settings.ini", QSettings.IniFormat)
        self.file, _ = QFileDialog.getOpenFileName(self, 'Open file', self.settings.value("dataset"), '*.json')
        self.clean_layout()
        if self.file and self.file.endswith(".json"):
            self.settings.setValue("dataset", self.file)
            self.sprite_editor_tab = ModeSelector()
            self.lay.addWidget(self.sprite_editor_tab)
            

    def clean_layout(self):
        for i in reversed(range(self.layout().count())): 
                self.layout().itemAt(i).widget().setParent(None)