from PyQt5.QtWidgets import QWidget, QVBoxLayout

class CentralWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_gui()
        self.show()
    
    def load_gui(self):
        self.lay = QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.lay)