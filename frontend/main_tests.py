from PyQt5.QtGui import QImage
from frontend.central_widget import CentralWidget
from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QLabel, QMainWindow, QPushButton, QRadioButton, QVBoxLayout, QWidget

from frontend.test_widget import TestWidget

import numpy as np
import random
import json



class ModeSelector(CentralWidget):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.filename = filename
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

        self.lay.addStretch()
        self.lay.addLayout(self.up_lay)
        self.lay.addLayout(self.down_lay)
        self.lay.addStretch()

        # Button functions
        self.random_mode_button.clicked.connect(self.create_random_test)
        self.real_test_button.clicked.connect(self.create_real_test)

    def create_random_test(self):
        self.test_window = Test(self.filename, "random")
        self.test_window.show()
        pass

    def create_real_test(self):
        self.test_window = Test(self.filename, "real")
        self.test_window.show()
        pass

class Answer(QWidget):
    def __init__(self, answer, button_group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_gui(answer, button_group)

    def load_gui(self, answer, button_group):
        self.lay = QHBoxLayout()
        self.radiobutton_lay = QVBoxLayout()
        self.radiobutton = QRadioButton(answer)
        
        self.status_lay = QVBoxLayout()
        self.status = QLabel()

        self.radiobutton_lay.addWidget(self.radiobutton)
        button_group.addButton(self.radiobutton)
        button_group.setId(self.radiobutton, len(button_group.buttons()) - 1)
        
        self.status_lay.addWidget(self.status)
        
        self.lay.addLayout(self.radiobutton_lay)
        self.lay.addLayout(self.status_lay)
        self.lay.addStretch()

        self.setLayout(self.lay)

class BaseTest(QWidget):
    def __init__(self, question, index, mem, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_gui(question[0], question[1], question[2])
        self.connect_signals(mem, index, question)

    def load_gui(self, question, answers : list, solution):
        self.lay = QVBoxLayout()
        self.question_lay = QHBoxLayout()
        self.question_label = QLabel(question)
        self.question_lay.addWidget(self.question_label)
        self.question_lay.setContentsMargins(10, 0, 0, 15)
        
        self.lay.addLayout(self.question_lay)
        self.button_group = QButtonGroup()

        for i in range(len(answers)):
            answer = Answer(answers[i], self.button_group)
            answer.setContentsMargins(0, 0, 0, 0)
            self.lay.addWidget(answer)
        
        self.buttons_lay = QHBoxLayout()
        self.previous = QPushButton("Previous")
        self.check = QPushButton("Check")
        self.next = QPushButton("Next")

        self.buttons_lay.addWidget(self.previous)
        self.buttons_lay.addStretch
        self.buttons_lay.addWidget(self.check)
        self.buttons_lay.addStretch
        self.buttons_lay.addWidget(self.next)

        self.buttons_lay.setContentsMargins(0, 20, 0, 0)

        self.lay.addLayout(self.buttons_lay)

        self.lay.addStretch()
        self.setLayout(self.lay)

    def connect_signals(self, mem, index, question):
        self.check.clicked.connect(lambda : self.check_answer(mem, index, question[2]))

    def check_answer(self, mem, index, solution):
        # Option checked | Solution
        mem[index] = [self.button_group.checkedId(), solution]
        print("Marcaste: ", mem[index][0], ", la solución es ", mem[index][1])


class Test(QMainWindow):
    def __init__(self, filename, test_type):
        super().__init__()

        with open(filename, encoding='utf-8') as jsonFile:
            self.data = tuple(json.load(jsonFile).items())
            jsonFile.close()

        self.questions = list()

        if test_type == "real":   
            rand_index = random.randint(0, len(self.data) - 1) 
            print(self.data[rand_index][0]) 
            for i in range(len(self.data[rand_index][1])):
                item = dict(self.data[rand_index][1][i])
                possible_answers = list(item['Answers'])
                answer = [item['Question'], possible_answers, item['Solution']]
                self.questions.append(answer)
        elif test_type == "random":
            pass

        self.memory = [[-1, -1]] * len(self.questions)
        self.questionIndex = 0
        self.load_question()
        

    def load_question(self):
        questionData = self.questions[0]
        questionWidget = BaseTest(questionData, self.questionIndex, self.memory)
        self.setCentralWidget(questionWidget)
        self.setContentsMargins(30, 20, 30, 20)