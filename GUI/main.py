import os, sys, csv,time,results
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UI(QDialog):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        self.source = "None"
        self.result_dir = "None"
        self.attack_type = "None"
        self.init_UI()

    def init_UI(self):

        self.labels = [QLabel(self) for _ in range(7)]
        self.originalPalette = QApplication.palette()
        
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        
        styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.results_button = QPushButton("Results")
        self.results_button.clicked.connect(self.open_attack_results)
        
        #Disable Run Widgets
        self.results_button.setDisabled(True)
        self.bottomRightGroupBox.setDisabled(True)
        self.topRightGroupBox.setDisabled(True)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(self.results_button)

        # Set main layout of GUI
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0, 1, 2)
        mainLayout.addWidget(self.topRightGroupBox, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("UI")
        self.changeStyle('macOS')
    

    def open_attack_results(self):
        self.w = results.Results(self.result_dir)
        self.w.show()
        self.results_button.setDisabled(True)
    

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)


    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox()

        def evaluate_Dropbox_Value():
            self.attack_type = self.attack_type_dropbox.currentText()
            if (self.attack_type != "None" or self.attack_type != "Select"):
                self.topRightGroupBox.setDisabled(False)
            
        # Widget Definition
        self.attack_type_dropbox = QComboBox()
        self.attack_type_dropbox.addItems(['Select','Spectre', 'Row-Hammer'])
        attack_type_label = QLabel("Attack Type")
        attack_type_label.setBuddy(self.attack_type_dropbox)
        self.attack_type_dropbox.activated.connect(evaluate_Dropbox_Value)

        #Widget Alignment
        attack_type_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Set the Layout
        layout = QVBoxLayout()
        layout.addWidget(attack_type_label)
        layout.addWidget(self.attack_type_dropbox)
        layout.addStretch(3)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()

        # Retrieve the selected file
        def get_file():
            dialog = QFileDialog()
            if dialog.exec():
                files = dialog.selectedFiles()
                self.source = files[0]
                file_selected.setText(os.path.basename(self.source))
                #Enable Run Widgets
                self.bottomRightGroupBox.setDisabled(False)

        # Widget definition
        upload_source_button = QPushButton('Upload')
        upload_source_button.clicked.connect(get_file)
        upload_source_button.setStyleSheet(
            "background-color: #D2042D;" +
            "border-style: outset;" +
            "border-width: 1px;" +
            "border-radius: 10px; " +
            "border-color: black;" + 
            "font: bold 11px;" +
            "min-width: 10em;padding: 6px")
        source_code_label = QLabel("Attack Source Code File")

        #Widget Alignmet 
        source_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_selected = QLabel("No file selected")
        file_selected.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Setting Layout
        layout = QVBoxLayout()
        layout.addWidget(source_code_label)
        layout.addWidget(file_selected)
        layout.addWidget(upload_source_button)
        self.topRightGroupBox.setLayout(layout)

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox()

        def run_attack():
            ssh_helper = os.getcwd() + "/Scripts/ssh_helper.sh"
            results_dir= os.getcwd() + "/Tmp/Spectre"
            name = self.attack_type + "_Attack_{}".format(time.strftime("%m%d-%H%M%S"))
            runs = runs_Input.text()
            wait_time = Wait_Time_Input.text()
            Test_mode = True
            Test_run = None
            
            # Simply runs the attack (runs) amount of times with (wait_time) sleep between each attack
            if(Test_mode == True):
                if (runs == "" and wait_time == ""):
                    os.system("sh " + ssh_helper +" {0} {1} {2} {3} {4} 1".format(results_dir,os.path.abspath(self.source),name,4,1))
                else:
                    os.system("sh " + ssh_helper +" {0} {1} {2} {3} {4} 1".format(results_dir,os.path.abspath(self.source),name,runs,wait_time))

            # Runs the attack 15 times with 5001 data points collected for each atttac and 5s sleep between each run
            
            else:
                if(Test_run == None): 
                    runs = 15
                os.system("sh " + ssh_helper + " {0} {1} {2} {3} {4} 0".format(results_dir,os.path.abspath(self.source),name,runs,1))
                processMLData(runs,name, results_dir)
                #os.system("sh model_helper.sh {0} {1} {2} {3} {4} 0".format(wd,source_file,name,runs,wait_time))
        
            #Set all the widgets Ready for the next Attack        
            self.result_dir = os.getcwd() + "/Tmp/Spectre/" + name + "/log.txt" 
            self.results_button.setDisabled(False)
            self.bottomRightGroupBox.setDisabled(True)
            self.attack_type_dropbox.setCurrentIndex(0)
            self.topRightGroupBox.setDisabled(True)
            Wait_Time_Input.setText("")
            runs_Input.setText("")
        
        ################################################################################################
        # Takes each data file, finds the difference (data[i+1]-data[i]), and puts them in a single csv
        # file where each row represents a set of power signature data.
        ################################################################################################
        # ARGUEMTN 1: numFiles      number of "data_#" power signature data files to process
        # ARGUMENT 2: name          name of the directory that contains the data files
        ################################################################################################
        
        def processMLData(numFiles, name, dir):
            output_file = dir + "/" + name + '/X_test_100.csv'
            outfile = open(output_file, 'w+', newline = '')
            writer = csv.writer(outfile)
            for i in range(numFiles):
                file = "{0}/{1}/data_{2}.txt".format(dir,name,i+1)
                with open(file, 'r') as f1:
                    data1 = list(csv.reader(f1))
                diff = [int(data1[i+1][0])-int(data1[i][0]) for i in range(len(data1)-1)]
                writer.writerow(diff)
        
        ################################################################################################
        # Method which Utilises Script to Remote on the the target laptop and collect various data
        # Needed by the Trained Model.

        ################################################################################################
        
        # Widget Defined # 
        run_button = QPushButton("Run Attack")
        run_button.clicked.connect(run_attack)
        run_button.setStyleSheet(
            "background-color: #D2042D;" +
            "border-style: outset;" +
            "border-width: 1px;" +
            "border-radius: 10px; " +
            "border-color: black;" + 
            "font: bold 11px;" +
            "min-width: 10em;padding: 6px")
        
        #Define Widgets
        Wait_Time_Label = QLabel("Wait Time Between Runs")
        Wait_Time_Input = QLineEdit()
        Runs_Label = QLabel("Number of Runs")
        runs_Input = QLineEdit()

        # Widget Alignments #
        Runs_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Wait_Time_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        runs_Input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Wait_Time_Input.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Setting Layout
        layout = QVBoxLayout()
        layout.addWidget(Runs_Label)
        layout.addWidget(runs_Input)
        layout.addWidget(Wait_Time_Label)
        layout.addWidget(Wait_Time_Input)
        layout.addWidget(run_button)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

        
    
if __name__ == '__main__':

    app = QApplication(sys.argv)
    GUI = UI()
    GUI.show()
    sys.exit(app.exec())
