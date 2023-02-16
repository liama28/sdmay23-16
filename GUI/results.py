import os
import sys
import csv,time
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QToolBar

class Results(QWidget):
    
    def __init__(self, _results_dir):
        super().__init__()
        self.result_dir = _results_dir
        self.open_results()
        
    def open_results(self):
        print(self.result_dir)
        f = open(self.result_dir, "r")
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        self.text = QTextEdit()
        self.text.setPlainText(f.read())
        layout.addWidget(self.text)
        self.setLayout(layout)