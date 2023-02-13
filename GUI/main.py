import os
import sys
import csv,time
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QFileDialog, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton,
                             QScrollBar, QSizePolicy, QSlider, QSpinBox,
                             QStyleFactory, QTableWidget, QTabWidget,
                             QTextEdit, QVBoxLayout, QWidget)

##################
# # Default values #
##################
# Working directory. Where the script is located
results_dir= "/Users/felipebautista/Programing_Workspaces/GUI/Tmp"
# The attack name
name = "ATR_{}".format(time.strftime("%m%d-%H%M%S"))

# For test run "-t"
# Number of times the attack will run
runs = 4
# The wait time between runs
wait_time = 1
Test_mode = True
Test_run = None



class UI(QDialog):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        self.labels = [QLabel(self) for _ in range(7)]
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(False)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        

        styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

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
        self.changeStyle('Windows')



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

        #Select Attack Type Dropdown
        attack_type_dropbox = QComboBox()
        attack_type_dropbox.addItems(['Select','Spectre', 'Row-Hammer'])
        attack_type_label = QLabel("Attack Type")
        attack_type_label.setBuddy(attack_type_dropbox)

        #Select Model Dropdown
        detection_model_dropbox = QComboBox()
        detection_model_dropbox.addItems(['Select','Model 1', 'Model 2'])
        detection_model_label = QLabel("Detection Model")
        detection_model_label.setBuddy(detection_model_dropbox)


         #Label Alignment
        attack_type_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        detection_model_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #Set the Layout
        layout = QVBoxLayout()
        layout.addWidget(attack_type_label)
        layout.addWidget(attack_type_dropbox)
        layout.addWidget(detection_model_label)
        layout.addWidget(detection_model_dropbox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()
    
        def get_file():
            dialog = QFileDialog()
            global source_file
            if dialog.exec():
                files = dialog.selectedFiles()
                source_file = files[0]
                file_selected.setText(os.path.basename(source_file))
                #textEditor.setPlainText(os.path.abspath(source_file))

        upload_source_button = QPushButton('Upload')
        upload_source_button.clicked.connect(get_file)
        source_code_label = QLabel("Attack Source Code")
        source_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_selected = QLabel("No file selected")
        file_selected.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(source_code_label)
        layout.addWidget(upload_source_button)
        layout.addWidget(file_selected)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    

        
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox()
        
        ################################################################################################
        # Takes each data file, finds the difference (data[i+1]-data[i]), and puts them in a single csv
        # file where each row represents a set of power signature data.
        ################################################################################################
        # ARGUEMTN 1: numFiles      number of "data_#" power signature data files to process
        # ARGUMENT 2: name          name of the directory that contains the data files
        ################################################################################################
        def processMLData(numFiles, name):
            output_file = name+'/X_test_100.csv'
            outfile = open(output_file, 'w', newline='')
            writer = csv.writer(outfile)
            for i in range(numFiles):
                file = "{0}/data_{1}.txt".format(name,i+1)
                with open(file, 'r') as f1:
                    data1 = list(csv.reader(f1))
                diff = [int(data1[i+1][0])-int(data1[i][0]) for i in range(len(data1)-1)]
                writer.writerow(diff)
        
        ################################################################################################
        # Method which Utilises Script to Remote on the the target laptop and collect various data
        # Needed by the Trained Model.

        ################################################################################################
        def run_attack():
            #########
            # START #
            #########
            # Simply runs the attack (runs) amount of times with (wait_time) sleep between each attack
            if(Test_mode == True):
                os.system("sh /Users/felipebautista/Programing_Workspaces/GUI/Scripts/ssh_helper.sh {0} {1} {2} {3} {4} 1".format(results_dir,os.path.abspath(source_file),name,runs,wait_time))
            

            # Runs the attack 15 times with 5001 data points collected for each atttac and 5s sleep between each run
            
           # else:
                #if(Test_run == None): 
                  #  runs = 15
                #os.system("sh ssh_helper.sh {0} {1} {2} {3} {4} 0".format(wd,source_file,name,runs,wait_time))
               # processMLData(runs,name)
               # os.system("sh model_helper.sh {0} {1} {2} {3} {4} 0".format(wd,source_file,name,runs,wait_time))
                #with open("{0}{1}/results.txt".format(wd,name), 'r') as f:
                  #  print(f.read())

            #textEditor.setPlainText(run)
            
            
        run = QPushButton("Run Attack")
        run.clicked.connect(run_attack)
        run_status = QLabel("Press to run Attack")
        run_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(run)
        layout.addWidget(run_status)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)
    

        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    gallery = UI()
    gallery.show()
    sys.exit(app.exec())
