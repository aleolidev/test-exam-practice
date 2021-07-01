from frontend.central_widget import CentralWidget
from PyQt5.QtWidgets import QWidget

import numpy as np
import json



class TestWidget(CentralWidget):
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = json.loads(filepath)
        print(self.data)

if __name__ == "__main__":
    a = TestWidget()


