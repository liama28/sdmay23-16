# Testing Workspace
This is the testing workspace used to launch experiments and collect data about instruction power consumption.

With this tool, you run attacks and get data back, like how well the ML model can detect the attack, its power signature, the number of instructions executed, and how long it took to run.

# Setup
Before you use the tool, both the machine learning server and testing laptop must be configured correctly, and the correct values are in the config.sh file. Follow the following steps to use the tool.

1. Establish a key pair for SSH authentication with the laptop and ML server
 - 'ssh-keygen'
 - 'ssh-copy-id <host>'
2. Create a working directory on the test laptop used to collect power signatures.
 - SSH into the laptop
 - Make a new directory on the laptop to store data and scripts.
 - Move all the files found in the "server_scripts" directory at the project's root into the new working directory.
 - Change the access permissions of all the files to allow execution
 - Configure sudo to run with "run_attack.sh"
3. Create a working directory on the ML server to classify power signatures
 - SSH into the server
 - Copy the model into another directory
4. Change the variables in the "config.sh" file to match the machine configurations.
