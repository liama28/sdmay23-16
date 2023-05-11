# Testing Workspace
This is the testing workspace used to launch experiments and collect data about instruction power consumption.

With this tool, you run attacks and get data back, like how well the ML model can detect the attack, its power signature, the number of instructions executed, and how long it took to run.

# Setup
Before you use the tool, both the machine learning server and testing laptop must be configured correctly, and the correct values are in the config.sh file. Follow the following steps to use the tool.

1. Establish a key pair for SSH authentication with the laptop and ML server
 - `ssh-keygen`
 - `ssh-copy-id <username>@<test_laptop_host>`
 - `ssh-copy-id <username>@<machine_learning_host>`
> **Note:** The tool will use your default ssh key. If you name the key something else or give it a password, the tool will not work.
2. Create a working directory on the test laptop used to collect power signatures.
 - Make a new directory on the laptop to store data and scripts.
 - Move all the files found in the "server_scripts" directory at the project's root into the new working directory.
  - `scp -r <project path>/server_scripts/* <username>@<test_laptop_host>:<workspace_path>`
 - Change the access permissions of all the files in the workspace to allow execution
  - `chmod +x *`
 - Configure sudo to run with "run_attack.sh"
  - `sudo visudo`
  - Append `<username> ALL=(ALL) NOPASSWD: <script_path>`
3. Create a working directory on the ML server to classify power signatures
 - Copy the model into another directory
  - `cp -r <ML_model_directory> <new_workspace>`
4. Change the variables in the "config.sh" file to match the machine configurations.
 - `TL_USERNAME=<laptop_username>`
 - `TL_HOST=<laptop_ip/hostname>`
 - `TL_WORKSPACE=<laptop_workspace_path>`
 - `MLS_USERNAME=<server_username>`
 - `MLS_HOST=<server_ip/hostname>`
 - `MLS_WORKSPACE=<server_workspace_path>`

 
