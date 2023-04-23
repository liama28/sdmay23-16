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
        self.console_display_string = ""
        self.errors_keywords = ["Quitting run..."]
        self.error_found = "False"
        self.ssh_helper_location = os.getcwd() + "/Scripts/ssh_helper.sh"
        self.model_helper_location = os.getcwd() + "/Scripts/model_helper.sh"
        self.init_UI()
    
    ################################################################################################
    # initializes UI components
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

        self.select_attack_type_function()
        self.file_upload_function()
        self.run_function()
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
    #Function to open a new window with the executed attack's results
    ################################################################################################
    def open_attack_results(self):
        self.w = results.Results(self.model_result_dir, self.attack_name)
        self.w.show()
        self.results_button.setDisabled(True)
    
    ################################################################################################
    # Function which all to change the style of the UI
    ################################################################################################
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    ################################################################################################
    # Function to change the Pallete of the UI
    ################################################################################################
    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)
    
    ################################################################################################
    # Function which create the console widget and initializes its attributes
    ################################################################################################        
    def create_console(self):
        self.console = QGroupBox()
    
        console_label = QLabel("Attack Execution Log")
        self.display = QLabel()

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.display)

        #Set the Layout
        layout = QVBoxLayout()
        layout.addWidget(console_label)
        layout.addWidget(self.display)
        self.console.setLayout(layout)
    
    ################################################################################################
    #
    ################################################################################################
    def select_attack_type_function(self):
        self.attack_selection_module = QGroupBox()

        ################################################################################################

        ################################################################################################
        def evaluate_Dropbox_Value():
            self.attack_type = self.attack_type_dropbox.currentText()
            if (self.attack_type == "None" or self.attack_type == "Select"):
                self.file_upload_module.setDisabled(True)
            else:
                self.file_upload_module.setDisabled(False)
                self.console_display_string = ""
                self.display.setText(self.console_display_string)
                
            
        # Widget Definition
        self.attack_type_dropbox = QComboBox()
        self.attack_type_dropbox.addItems(['Select','Spectre'])
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
    def file_upload_function(self):
        self.file_upload_module = QGroupBox()

        ################################################################################################
        # Allows user to upload the source code of their attack
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
    def run_function(self):
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
            outfile = open(output_file, 'w+', newline = '')
            writer = csv.writer(outfile)
            for i in range(numFiles):
                file = "{0}/{1}/data_{2}.txt".format(dir,name,i+1)
                with open(file, 'r') as f1:
                    data1 = list(csv.reader(f1))
                diff = [int(data1[i+1][0])-int(data1[i][0]) for i in range(len(data1)-1)]
                writer.writerow(diff)
            

        def check_parameters(self):
            if (use_default_parameters.isChecked()):
                use_default_parameters.setChecked(True)
                Wait_Time_Input.setDisabled(True)
                runs_Input.setDisabled(True)
            else:
                use_default_parameters.setChecked(False)
                Wait_Time_Input.setDisabled(False)
                runs_Input.setDisabled(False)
        
        ################################################################################################
        # Function to reset all necessary widgets before a new attack is ran
        ################################################################################################
        def reset_widgets():
            if(self.error_found == "False"):
                self.results_button.setDisabled(False)
            self.run_attack_module.setDisabled(True)
            self.attack_type_dropbox.setCurrentIndex(0)
            self.file_upload_module.setDisabled(True)
            self.error_found = "False"

        ################################################################################################
        # Function
        ################################################################################################    
        def read_attack_log(dir):
            for error in self.errors_keywords:
                search_errors(dir,error)
            self.display.setText(self.console_display_string)  
        
        ################################################################################################

        ################################################################################################
        def search_errors(dir,word):
            with open(dir, 'r') as fp:
            #read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find(word) != -1:
                        self.console_display_string += line + '\n'
                        self.error_found = 'True'
                    else:
                        self.error_found = 'False'
            if(self.error_found == "False"):
                self.console_display_string = "Execution Successful"            

        
        ################################################################################################

        ################################################################################################
        def run_attack():
            results_folder = os.getcwd() + "/Results/" + self.attack_type_dropbox.currentText()
            self.attack_name = self.attack_type + "_Attack_{}".format(time.strftime("%m%d-%H%M%S"))
            runs = runs_Input.text()
            wait_time = Wait_Time_Input.text()
            Test_mode = False
        
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
                if(use_default_parameters.isChecked()): 
                    
                    os.system("sh " + self.ssh_helper_location + 
                          " {0} {1} {2} {3} {4} 0 >> {5}_log.txt".format(results_folder,os.path.abspath(self.source),self.attack_name,15,1,self.attack_name))
                    os.system("mv {0}_log.txt {1}/{2}".format(self.attack_name,results_folder,self.attack_name))
                    log_file_directory = results_folder + "/" + self.attack_name + "/" + self.attack_name + "_log.txt"
                    read_attack_log(log_file_directory)
                    if(self.error_found == "False"):
                        processMLData(15,self.attack_name, results_folder)
                        os.system("sh " + self.model_helper_location + 
                          " {0} {1} {2} {3} {4} 0".format(results_folder,os.path.abspath(self.source),self.attack_name,15,1,self.attack_name))
                
                else:
                    print("2")

            
            self.model_result_dir = results_folder + "/" + self.attack_name + "/results.txt" 
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
        use_default_parameters = QCheckBox("Use Default Parameters")
        use_default_parameters.setChecked(True)
        use_default_parameters.toggled.connect(check_parameters)
        
        Wait_Time_Label = QLabel("Wait Time Between Runs")
        Wait_Time_Input = QLineEdit()
        Wait_Time_Input.setDisabled(True)
        Runs_Label = QLabel("Number of Runs")
        runs_Input = QLineEdit()
        runs_Input.setDisabled(True)

        # Widget Alignments #
        Runs_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Wait_Time_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        runs_Input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Wait_Time_Input.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Setting Layout
        layout = QVBoxLayout()
        layout.addWidget(use_default_parameters)
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
