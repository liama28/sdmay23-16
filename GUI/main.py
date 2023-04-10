import os, sys, csv,time,results
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class UI(QDialog):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        self.source = "None"
        self.model_result_dir = "None"
        self.attack_type = "None"
        self.attack_name = "None"
        self.ssh_helper_location = os.getcwd() + "/Scripts/ssh_helper.sh"
        self.model_helper_location = os.getcwd() + "/Scripts/model_helper.sh"
        self.init_UI()
    
    ################################################################################################

    ################################################################################################
    def init_UI(self):

        self.labels = [QLabel(self) for _ in range(7)]
        self.originalPalette = QApplication.palette()
        
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        self.create_attack_selection_module()
        self.create_File_Upload_Module()
        self.create_Run_Attack_Module()
        self.create_console()
        
        styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.results_button = QPushButton("Results")
        self.results_button.clicked.connect(self.open_attack_results)
        
        #Disable Run Widgets
        self.results_button.setDisabled(True)
        self.run_attack_module.setDisabled(True)
        self.file_upload_module.setDisabled(True)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(self.results_button)

        # Set main layout of GUI
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.attack_selection_module, 1, 0, 1, 2)
        mainLayout.addWidget(self.file_upload_module, 2, 0)
        mainLayout.addWidget(self.run_attack_module, 2, 1)
        mainLayout.addWidget(self.console, 3,0,1,2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("UI")
        self.changeStyle('macOS')
    
    ################################################################################################

    ################################################################################################
    def open_attack_results(self):
        self.w = results.Results(self.model_result_dir, self.attack_name)
        self.w.show()
        self.results_button.setDisabled(True)
    
    ################################################################################################

    ################################################################################################
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    ################################################################################################
    #
    ################################################################################################
    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)
    
    ################################################################################################
    # 
    ################################################################################################        
    def create_console(self):
        self.console = QGroupBox()
    
        console_label = QLabel("Attack Execution Log")
        self.display = QTextEdit()

        console_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Set the Layout
        layout = QVBoxLayout()
        layout.addWidget(console_label)
        layout.addWidget(self.display)
        self.console.setLayout(layout)
    
    ################################################################################################
    #
    ################################################################################################
    def create_attack_selection_module(self):
        self.attack_selection_module = QGroupBox()

        ################################################################################################

        ################################################################################################
        def evaluate_Dropbox_Value():
            self.attack_type = self.attack_type_dropbox.currentText()
            if (self.attack_type == "None" or self.attack_type == "Select"):
                self.file_upload_module.setDisabled(True)
            else:
                self.file_upload_module.setDisabled(False)
                
            
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
        self.attack_selection_module.setLayout(layout)

    ################################################################################################

    ################################################################################################
    def create_File_Upload_Module(self):
        self.file_upload_module = QGroupBox()

        ################################################################################################

        ################################################################################################
        def get_file():
            dialog = QFileDialog()
            if dialog.exec():
                files = dialog.selectedFiles()
                self.source = files[0]
                file_selected.setText(os.path.basename(self.source))
                #Enable Run Widgets
                self.run_attack_module.setDisabled(False)

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
        self.file_upload_module.setLayout(layout)
    
    ################################################################################################

    ################################################################################################
    def create_Run_Attack_Module(self):
        self.run_attack_module = QGroupBox()

        ################################################################################################
        # Takes each data file, finds the difference (data[i+1]-data[i]), and puts them in a single csv
        # file where each row represents a set of power signature data.
        ################################################################################################
        # ARGUEMTN 1: numFiles      number of "data_#" power signature data files to process
        # ARGUMENT 2: name          name of the directory that contains the data files
        ################################################################################################
        
        def processMLData(numFiles, name, dir):
            output_file = dir + "/" + name + '/X_attack_test_15.csv'
            try:
                outfile = open(output_file, 'w+', newline = '')
                writer = csv.writer(outfile)
                for i in range(numFiles):
                    file = "{0}/{1}/data_{2}.txt".format(dir,name,i+1)
                    with open(file, 'r') as f1:
                        data1 = list(csv.reader(f1))
                    diff = [int(data1[i+1][0])-int(data1[i][0]) for i in range(len(data1)-1)]
                    writer.writerow(diff)
            except IOError:
                self.display.setText("Detected Attack Running: Run Failed")
        
        ################################################################################################

        ################################################################################################
        def reset_widgets():
            self.results_button.setDisabled(False)
            self.run_attack_module.setDisabled(True)
            self.attack_type_dropbox.setCurrentIndex(0)
            self.file_upload_module.setDisabled(True)

        ################################################################################################

        ################################################################################################    
        def read_attack_log(dir):
            log = open(dir, "r").read()
            self.display.setText(log)  
        
        ################################################################################################

        ################################################################################################
        def run_attack():
            results_folder = os.getcwd() + "/Results/" + self.attack_type_dropbox.currentText()
            self.attack_name = self.attack_type + "_Attack_{}".format(time.strftime("%m%d-%H%M%S"))
            runs = runs_Input.text()
            wait_time = Wait_Time_Input.text()
            Test_mode = False
            Test_run = None
        
            self.display.setText("")
            # Simply runs the attack (runs) amount of times with (wait_time) sleep between each attack
            if(Test_mode == True):
                if (runs == "" and wait_time == ""):
                    os.system("sh " + self.ssh_helper_location + 
                              " {0} {1} {2} {3} {4} 1".format(results_folder,os.path.abspath(self.source),self.attack_name,4,1))
                else:
                    os.system("sh " + self.ssh_helper_location + 
                              " {0} {1} {2} {3} {4} 1".format(results_folder,os.path.abspath(self.source),self.attack_name,runs,wait_time))

            # Runs the attack 15 times with 5001 data points collected for each atttac and 5s sleep between each run
            
            else:
                if(Test_run == None): 
                    runs = 15
                os.system("sh " + self.ssh_helper_location + 
                          " {0} {1} {2} {3} {4} 0 >> {5}_log.txt".format(results_folder,os.path.abspath(self.source),self.attack_name,runs,1,self.attack_name))
                processMLData(runs,self.attack_name, results_folder)
                os.system("sh " + self.model_helper_location + 
                          " {0} {1} {2} {3} {4} 0".format(results_folder,os.path.abspath(self.source),self.attack_name,runs,1,self.attack_name))
        
            os.system("mv {0}_log.txt {1}/{2}".format(self.attack_name,results_folder,self.attack_name))    
            self.model_result_dir = results_folder + "/" + self.attack_name + "/results.txt" 
            log_file_directory = results_folder + "/" + self.attack_name + "/" + self.attack_name + "_log.txt"
            read_attack_log(log_file_directory)
            reset_widgets()
            Wait_Time_Input.setText("")
            runs_Input.setText("")
            
        
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
        self.run_attack_module.setLayout(layout)

        
    
if __name__ == '__main__':

    app = QApplication(sys.argv)
    GUI = UI()
    GUI.show()
    sys.exit(app.exec())
