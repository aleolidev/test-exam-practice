from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QFileDialog
from PyQt5.QtWidgets import QShortcut, QSizePolicy, QColorDialog, QPushButton
from PyQt5.QtGui import QPixmap, QKeySequence, QColor, QCursor
from PyQt5.QtCore import Qt, QMargins, QUrl, pyqtSignal

import numpy as np



class ModeSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.up_lay = QHBoxLayout()

        self.random_mode_button = QPushButton('Random Mode', self)
        self.up_lay.addStretch()
        self.up_lay.addWidget(self.random_mode_button)
        self.up_lay.addStretch()

        self.down_lay = QHBoxLayout()

        self.real_test_button = QPushButton('Real Test', self)
        self.down_lay.addStretch()
        self.down_lay.addWidget(self.real_test_button)
        self.down_lay.addStretch()

        self.lay = QVBoxLayout()
        self.lay.addStretch()
        self.lay.addLayout(self.up_lay)
        self.lay.addLayout(self.down_lay)
        self.lay.addStretch()
        self.setLayout(self.lay)

if __name__ == "__main__":
    a = ModeSelector()


