# Spectre Attack GUI 


## Setup & Procedures:

### Prerequisites:
This program requires the Python 3.x and PyQt6 packages.


### Makefile:
To install the Required dependencies run the following command in the shell of your choice:

                 $   sudo make install
                 
To compile the source files exxecute the following command:

                 $   sudo make
                 
To run the code it's as simple as typing the following into your shell:

                 $   spectreGUI

To remove the executable and all unnecessary object files run the folling:

                 $   sudo make clean



## Generic Preference File: ipaddr.cfg |

### Description:
A CFG file is a generic preference file that stores settings and configuration information. In this case it holds the current IP address of the remove server. It is used in both the ssh_helper and model_helper bash scripts. It contains one line of code and an example of the IP address used to connect to the remote server can be seen below under the "Usage:" section.

### Usage:
Since the IP address of the remote server will change more than once during the course of this project, this is a simple configuration file to make adapting to IP address changes more streamlined. Without this file, the IP address would have to be manually changed in mutiple places across the two bash scripts: "model_helper.sh" and "ssh_helper.sh". As mentioned previously it is one line of code similar to the following: 
 
                 IPADDR=10.26.XXX.XXX
   
NOTE: "XXX" denotes values that can change in the IP address.


## SSH Key Generation:
The Learning Model and Remote Server, both, require the use of SSH for connecting remotley from your personal computer. By setting up an SSH Key Pair, the system will not prompt you for a password every time you attempt to make a connection through the shell. Additonally, without the SSH Key the GUI will throw several errors when attempting to make a connection. Below, I will list the steps neccessary for generating your own SSH key as well as setting up an SSH key pair on both servers. 

NOTE: Depedning on your personal OS and setup, you may need to use sudo permissions. Do not use them unless neccessary here.

NOTE: The IP may change several times during the course of this project.

NOTE: "$" can often denote a new line in the console when reffering to Shell commands and occasionlly when reffering to bash scripting.


### SETTING UP AN SSH KEY PAIR:

  Step (01): Generate your own personal SSH Key.
    - Run the following command in the shell of your choice.
    
                 $   ssh-keygen
    
   Step (02): Copy your newly generated SSH Key onto the Remote Server.
     - Run the following command in the shell of your choice. 
                 
                 $   ssh-copy-id sdmay23-16@10.26.XXX.XXX
   
   Step (03): Copy your SSH Key onto the Machine Learning Model's Server.
     - Run the following command in the shell of your choice. 
                 
                 $   ssh-copy-id sdmay23-16@berk.ece.iastate.edu


## Running the Program:
First open a shell of your choice and chage directories until you are in the project folder named "GUI" that actually contains the GUI's python scripts. Do this by executing the following command in the shell of your choice:

                 $   cd ~/{file_path_to_sdmay23-16-main}/sdmay23-16-main/GUI
                 
NOTE: {file_path_to_sdmay23-16-main} will vary based on where you have the project saved on your local machine.

To Confirm you are in the correct place, you may run either of the following two commands:

                 $   pwd    // pwd - post working directory displays the filepath
                            // your curent location in the shell.
                 or
                 
                 $   ls     // list- shows you the contents of the directory your
                            // shell is currently in. If using this method, make
                            // sure at the very least the file "main.py" is
                            // present.
                 
                 
To run the program, execute the following command in the shell of your choice:

                 $   sudo python3 main.py



# Python Scripts:

## FILE: main.py |
### Description: 
This is a graphical user interface (GUI) for executing the Spectre attack. The main file running the GUI is called "main.py." The program consists of a UI class that allows users to select an attack type and upload a file to execute the selected attack. The program's UI is styled with Qt and can be customized using the style selection dropdown menu.
    

### UI Components:
The UI class consists of the following components:
    - Attack Type Selection Module
    - File Upload Module
    - Run Attack Module
    - Results Button
    - Console Widget
    
    
### Functionality:
The init_UI() function initializes the following components:
    - Labels
    - Style combo box
    - Check box
    - Attack type selection
    - File upload    
    - Run attack    
    - Console

The other functions handle the following:    
    - open_attack_results(): Opens a new window with the executed attack's results.
    
    - changeStyle(): Allows changing the style of the UI.
    
    - changePalette(): Allows changing the palette of the UI.
    
    - create_console(): Creates a console widget to display the attack execution log. It initializes its attributes, such as the console label and display label, and sets their style using CSS. The console widget is added to the main layout along with other UI components.
    
    - select_attack_type_function(): Creates the attack type selection module and initializes its attributes. It adds a combo box to select the attack type and sets a listener function to detect changes in the selection. If the selected attack type is "None" or "Select," the file upload module is disabled. Otherwise, the file upload module is enabled and the console display string is reset. The attack type selection module is added to the main layout along with other UI components.
    
    - file_upload_function(): Creates the file upload module and initializes its attributes. It adds a button to allow users to upload their attack source code file and sets a listener function to handle the file upload. The selected file name is displayed on the module. The run attack module is enabled once the file is uploaded. The file upload module is added to the main layout along with other UI components.
    
    - run_function(): Creates the run attack widget and initializes its attributes. The run attack module is a QGroupBox that takes each data file, finds the difference (data[i+1]-data[i]), and puts them in a single CSV file where each row represents a set of power signature data. It consists of a listener function to evaluate which set of parameters to use based on the checkbox, a function to reset all necessary widgets before a new attack is run, and a function to scan the log file generated by the ssh script and search for errors. If no errors are found, the results button is enabled. The run attack module is added to the main layout along with other UI components.

    - search_errors(): This helper function is used by the run_function() to scan the log file generated by the ssh script and search for errors. It takes the directory of the log file and an error keyword to look for in a file as arguments. It reads all lines in the file, searches for the keyword, and sets a flag if the error is found. If no errors are found, it sets the console display string to "Execution Successful".

    - run_attack(): This function runs a given attack using the given parameters by the user. It sets the results folder and attack name based on the user's selections and time. It gets the number of runs, wait time, and Test_mode value from their respective input fields. If Test_mode is True, the attack runs the given number of times with the given wait time between each run. If Test_mode is False and the default parameters checkbox is selected, the attack runs 15 times with 5001 data points collected for each attack and a 5 second sleep between each run. The log file generated by the ssh script is moved to the results folder, and the console display string is set to "Execution Successful" if no errors are found in the log file. The run attack module is added to the main layout along with other UI components.



## FILE: notify.py

### Description:
This is a python script that defines a "Notify" class used to display warning messages in the GUI. It takes three arguments as parameters: condition, message, and detailed_text. It intalizes these arguments as local varaible using "self.{var_name}". If condition is True, the class shows a warning message box with message. If detailed_text is provided, it is displayed in the detailed text section of the message box.


### Usage: 
To use this class in a Python script, such as "main.py", create a "Notify" object with the appropriate arguments, and then call the show method on the newly created object. For example, to show a warning message with the message: "Your warning message here" and the detailed text: "Additional information about the warning can be displayed here." when the condition is True, the following code can be used to display an error:

   $ notify = Notify(True, "Your warning message here", "Additional information about the warning can be displayed here.")

   $ notify.show()


### Functionality:    
    - show(): This function displays a message box and prompts the user for a response. If the user clicks the "Ok" button, the message "Thank you, further details can be seen in the console." is printed to the error console. If the user clicks the "Ignore" button, the message "The warning has been ignored, please take caution while proceeding." is printed in the console.
    
    
### Issues & Bugs:
This was one of the latter aspects implmented into the GUI. The issue present is that the detailed_text provided as input is not properly displaying to the Log Console. The "show" function otherwise still works as intended. The lack of it actually displaying anything in the console does not currently cause any additional bugs in the GUI. Due to the time constraints of senior design, the issue is present in our current iteration of the software. The root cause is currently still unknown. Aditionally, (for the same reasons) the process of researching and implmenting a work-around or potential solution fell out of our scope.



## FILE: results.py

### Description: 
A Python script that defines a "Results" class. This class is a PyQt6 widget that displays the results of a given attack. It takes two parameters on initialization, _results_dir and _attack_name. _results_dir is a string that specifies the directory where the results file is located. _attack_name is a string that specifies the name of the attack. The "Results" widget is then created and laid out using a QGridLayout. The title and results group boxes are then added to the layout and the window title is set to "Results".


### Usage:
The results class is called by the open_attack_results function in "main.py" to open a new window with the executed attack's results displayed within.


### Functionality:    
    - The define_attack(): This method creates a QGroupBox widget that contains the title of the results page. It takes no parameters and sets the Title attribute of the Results class.

    - open_results(): This method creates a QGroupBox widget that contains the actual results of the attack. It reads the contents of the results file specified by _results_dir and displays it in a QLabel. The QLabel is then placed in a QScrollArea to enable scrolling in a situation where the contents of the file are larger than the actual window's size. The results_layout attribute of the "Results" class is set to the newly created QGroupBox widget.



# Attack Code:

## Source File: Source.c

### Description:
This code demonstrates the Spectre attack by exploiting a side-channel information leakage vulnerability. It shows how an attacker can use timing measurements to infer secret information from a victim process.


### Usage:
The file contains the source code for the victim and analysis portion of the Spectre attack. 

Victim Code: 
In this section of code, an array called "array1" is defined with a size of 160 bytes. This array is used to store a set of integers (1-16). There is also an array called "array2" with a size of 256 * 512 bytes. The variable "temp" is used to prevent the compiler from optimizing out the victim_function().

Analysis Code:
In this section of code, the readMemoryByte() function takes a size_t variable "malicious_x" and two arrays "value" and "score" as input. It sets an array "results" with 256 integers to 0 and initializes some variables. It then flushes the array2 from the cache, runs some training loops to reduce measurement noise, and then runs the victim_function() with the "malicious_x" input value. After this, it measures the time it takes to read from the array2 for each element in the array2, and updates the "results" array based on whether the read time is less than or equal to a predefined CACHE_HIT_THRESHOLD value. It repeats these steps several times and determines the highest and second-highest results in the "results" array. Finally, it returns the two values with the highest and second-highest results as well as their corresponding scores.

### Functionality:
    - victim_function(): This function takes a size_t variable "x" as input and checks if x is less than the size of array1. If x is less than the size of array1, it multiplies the value stored in array1[x] with 512. The result is used as an index in array2 to access the value at the specified index.
    
    - main(): The "main" function initializes array2 by writing '1's to its elements. It takes two arguments from the command line: a hexadecimal value that represents the address of the secret string (initialized in the victim code section), and an integer that represents the number of bytes to read from the secret string. If these arguments are not provided, the default values are used. The "main" function then calls the readMemoryByte() function in a loop. 

    - readMemoryByte(): This function (called from "main" in a loopa) is used to read each byte of the secret string, print the value of the byte, and its corresponding score.
    


# Bash Scripts:


## Script: model_helper.sh

### Description:
This is a bash script that helps in running attacks and collecting data for machine learning model's creation. The script takes six arguments and three constant values which will be described in more detail below, under the section "Functionality: Arguments & Constant Values".



### Usage: 
The script first changes into the working directory and then uses the scp command to copy the X_attack_test_15.csv file from the current attack run's directory to the ~/testing_workspace/Data/ directory on the ML server. Next, the script uses the ssh command to log into the ML server and execute the Restored_model_test.py script located in the testing_workspace directory. The >> operator is used to append the output of the Restored_model_test.py script to a file named results_NAME.txt, where NAME is the name of the current attack test run. The deactivate command is then used to exit the virtual environment created by source tensorflow/roy-venv/bin/activate. Finally, the script uses the scp command to copy the results_NAME.txt file from the ML server back to the current attack run's directory.

    
### Functionality: Arguments & Constant Values
Arguments:
    
    - SOURCE_DIR: The working directory for the source files.
    
    - SOURCE_FILE: The name of the source file for the attack, relative to the SOURCE_DIR.
    
    - NAME: The name of the attack test run.
    
    - RUNS: The number of times to run the attack.
    
    - WAIT_TIME: The wait time between each attack for simple attack runs.
    
    - TEST: A boolean value that is 0 if the script should collect data for the ML model, and 1 if the script should run a simple attack.
    
    
Constant Variables:
    
    - TL_USERNAME: The username for the remote test laptop.
    
    - MLS_USERNAME: The username for the ML server.
    
    - MLS_HOST: The hostname or IP address of the ML server.
        


## Script: ssh_helper.sh

### Description:
This is a bash script that assists in the automation of running an attack remotely on a target machine and collecting the results. The script takes in six arguments and five constant values which will be described in more detail below, under the section "Functionality: Arguments & Constant Values".


### Usage:
First, the script sets up the ssh info for the remote test laptop and the ML server before it creates a directory for the attack. It then makes the directory on the remote machine server and copies the source code of the attack onto the remote machine. Lastly, this script runs the attack remotely on the target machine and copies the results back to the host machine.

    
### Functionality: Arguments & Constant Values 
Arguments:
    - SOURCE_DIR: the directory of the attack source file
    
    - SOURCE_FILE: the path to the source file for the attack. This is relative to the SOURCE_DIR
    
    - NAME: the name of the attack test run
    
    - RUNS: the number of times to run the attack
    
    - WAIT_TIME: the wait time between each attack for simple attack runs
    
    - TEST: 0 or 1. 0 means collect data for the machine learning model, while 1 means to run a simple attack
    
    
Constant Variables:
    - TL_USERNAME: the username for the remote test laptop
    
    - TL_HOST: the IP address of the remote test laptop
    
    - MLS_USERNAME: the username for the machine learning server
    
    - MLS_HOST: the hostname of the machine learning server
    
    - FILE_NAME: the name of the attack source code file
    


# Credits & Contributions:
	Iowa State University & Senior Design Group Sdmay16_23


