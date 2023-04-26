
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Results(QWidget):
    
    def __init__(self, _results_dir, _attack_name):
        super().__init__()
        self.result_dir = _results_dir
        self.attack_name = _attack_name
        
        self.define_attack()
        self.open_results()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.Title, 1, 0)
        mainLayout.addWidget(self.results_layout, 2, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle("Results")
    
    ######################################################################
    # Function to set the page display components to the correct attack
    ######################################################################
    def define_attack(self):
        self.Title = QGroupBox()
        label = QLabel("")
        label.setText(self.attack_name + " Results")    

        layout = QVBoxLayout()
        layout.addWidget(label)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.Title.setLayout(layout)

    ######################################################################
    # Function to open the attack's result file and display it on the page
    ######################################################################  
    def open_results(self):
        self.results_layout = QGroupBox()

        file = open(self.result_dir, "r").read()
        
        display_file = QLabel(file)

        scrollArea = QScrollArea()
        scrollArea.setWidget(display_file)
        
        layout = QVBoxLayout()
        layout.addWidget(scrollArea)
        
        self.results_layout.setLayout(layout)