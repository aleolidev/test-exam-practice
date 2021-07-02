from frontend.central_widget import CentralWidget
from PyQt5.QtWidgets import QButtonGroup, QHBoxLayout, QInputDialog
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QRadioButton, 
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox

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

        self.real_test_button = QPushButton('Test Set', self)
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

        self.radiobutton_lay.addWidget(self.radiobutton)
        button_group.addButton(self.radiobutton)
        button_group.setId(self.radiobutton, len(button_group.buttons()) - 1)
        
        self.lay.addLayout(self.radiobutton_lay)
        self.lay.addStretch()

        self.setLayout(self.lay)

class BaseTest(QWidget):
    def __init__(self, test, question, index, mem,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_gui(test, question, index, mem)
        self.connect_signals(test, mem, index, question)

    def load_gui(self, test, question, index, mem):
        self.lay = QVBoxLayout()
        self.question_lay = QHBoxLayout()
        self.question_label = QLabel(str(index + 1) + ". "  + question[0])
        self.question_lay.addWidget(self.question_label)
        self.question_lay.setContentsMargins(10, 0, 0, 15)
        
        self.lay.addLayout(self.question_lay)
        self.button_group = QButtonGroup()

        for i in range(len(question[1])):
            answer = Answer(question[1][i], self.button_group)
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

        # total_questions, answered_questions, correct_answers

        total_questions = len(mem)
        answered_questions = self.answered_questions(mem)
        correct_answers = self.correct_answers(mem)

        current_mark = ""
        if answered_questions > 0:
            current_mark = str(float(correct_answers/answered_questions) * 10)
        
        overall_mark = ""
        if answered_questions > 0:
            overall_mark = str(float(correct_answers/total_questions) * 10)



        self.status_lay = QHBoxLayout()
        self.status_label = QLabel(
            "Answered questions: " + str(answered_questions) + "/" + str(total_questions) +
            "  |  Correct over answered: " + str(correct_answers) + "/" + str(answered_questions) +
            "  |  Current mark: " + current_mark  +
            "  |  Overall mark: " + overall_mark
        )

        self.status_lay.addStretch()
        self.status_lay.addWidget(self.status_label)
        self.status_lay.addStretch()
        self.status_lay.setContentsMargins(0, 15, 0, 0)
        self.lay.addLayout(self.status_lay)

        # Checks
        if index <= 0:
            self.previous.setDisabled(True)

        if index >= (len(mem) - 1):
            self.next.setDisabled(True)

        if mem[index][0] > -1 or mem[index][1] > -1:
            self.check.setDisabled(True)
            for i, button in enumerate(self.button_group.buttons()):
                if i == mem[index][0]:
                    button.setChecked(True)
                    button.setStyleSheet("color : #D13737!important")
                if i == mem[index][1]:
                    button.setStyleSheet("color : #3AB449!important") 
                button.setDisabled(True)

        self.lay.addStretch()
        self.setLayout(self.lay)

        if answered_questions >= total_questions and not test.results_already_showed:
            test.results_already_showed = True
            self.show_results(mem, total_questions, correct_answers, overall_mark)



    def connect_signals(self, test, mem, index, question):
        self.check.clicked.connect(lambda : self.check_answer(mem, index, question[2], test))
        self.previous.clicked.connect(test.previous_page)
        self.next.clicked.connect(test.next_page)

    def check_answer(self, mem, index, solution, test):
        # Option checked | Solution
        mem[index] = [self.button_group.checkedId(), solution]
        test.load_question()

    def answered_questions(self, mem):
        counter = 0
        for item in mem:
            if item[1] > -1:
                counter += 1
        
        return counter

    def true_answered_questions(self, mem):
        counter = 0
        for item in mem:
            if item[0] > -1:
                counter += 1
        
        return counter

    def correct_answers(self, mem):
        counter = 0
        for item in mem:
            if item[0] != -1 and item[0] == item[1]:
                counter += 1
        
        return counter
    
    def show_results(self, mem, total_questions, correct_answers, overall_mark):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        true_answered_questions = self.true_answered_questions(mem)

        mark_over_answered = ""
        if true_answered_questions > 0:
            mark_over_answered = str(float(correct_answers/true_answered_questions) * 10)

        msg.setText(
            "Answered questions: " + str(true_answered_questions) + "/" + str(total_questions) + "\n" +
            "Correct over answered: " + str(correct_answers) + "/" + str(true_answered_questions) + "\n" +
            "Correct over all: " + str(correct_answers) + "/" + str(total_questions) + "\n" +
            "Mark over answered: " + mark_over_answered + "\n" +
            "Mark: over all: " + overall_mark
        )

        msg.setInformativeText("Look at the details to see your mark if the questions will remove points.")
        msg.setWindowTitle("Test results")

        # Detailed marks string construction

        detailed_text = ""
        wrong_answers = true_answered_questions - correct_answers
        for i in range(1, 7):
            mark = overall_mark
            if wrong_answers > 0 and total_questions > 0:
                mark = float((correct_answers - (wrong_answers/i))/total_questions) * 10
                
            detailed_text += str(i) + " bad take away 1 good: " + str(mark) + "\n"

        msg.setDetailedText(detailed_text)

        msg.exec_()

class Test(QMainWindow):
    def __init__(self, filename, test_type):
        super().__init__()

        with open(filename, encoding='utf-8') as jsonFile:
            self.data = tuple(json.load(jsonFile).items())
            jsonFile.close()

        self.questions = list()
        self.results_already_showed = False

        if test_type == "real":   
            rand_index = random.randint(0, len(self.data) - 1) 
            print(self.data[rand_index][0]) 
            for i in range(len(self.data[rand_index][1])):
                item = dict(self.data[rand_index][1][i])
                answer = [item['Question'], list(item['Answers']), item['Solution']]
                self.questions.append(answer)
        elif test_type == "random":
            max_questions = self.get_max_questions()
            questions_amount = self.get_questions_amount(max_questions)

            question_indices = set()

            questions_str = ""
            while len(question_indices) < questions_amount:
                rand_int = random.randint(0, max_questions-1)
                question_indices.add(rand_int)
                questions_str += str(rand_int) + ", "

            print("Questions: ", questions_str)

            raw_questions = list()
            overall_counter = 0
            for i in range(len(self.data)):
                for j in range(len(self.data[i][1])):
                    item = dict(self.data[i][1][j])
                    answer = [item['Question'], list(item['Answers']), item['Solution']]
                    raw_questions.append(answer)

            for idx in question_indices:
                self.questions.append(raw_questions[idx])

        self.memory = [[-1, -1]] * len(self.questions)
        self.questionIndex = 0
        self.load_question()
        
    def next_page(self):
        if self.questionIndex < len(self.questions) - 1:
            self.questionIndex += 1
            self.load_question()

    def previous_page(self):
        if self.questionIndex > 0:
            self.questionIndex -= 1
            self.load_question()

    def load_question(self):
        questionData = self.questions[self.questionIndex]
        questionWidget = BaseTest(self, questionData, self.questionIndex, self.memory)
        self.setCentralWidget(questionWidget)
        self.setContentsMargins(30, 20, 30, 20)

    def get_max_questions(self):
        counter = 0
        for item in self.data:
            counter += len(item[1])

        return counter

    def get_questions_amount(self, max):
        i, okPressed = QInputDialog.getInt(self, "Get Integer", "Questions amount:", max, 1, max, 1)
        if okPressed:
            return i
        else:
            return -1