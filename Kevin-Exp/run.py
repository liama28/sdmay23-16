import argparse
import os
import time
import csv

##################
# Default values #
##################
# Working directory. Where the script is located
wd = os.getcwd() + "/"
# The attack name
name = "ATR_{}".format(time.strftime("%m%d-%H%M%S"))

# For test run "-t"
# Number of times the attack will run
runs = 4
# The wait time between runs
wait_time = 1

################################################################################################
# Takes each data file, finds the difference (data[i+1]-data[i]), and puts them in a single csv
# file where each row represents a set of power signature data.
################################################################################################
# ARGUEMTN 1: numFiles      number of "data_#" power signature data files to process
# ARGUMENT 2: name          name of the directory that contains the data files
################################################################################################
def processMLData(numFiles, name):
    output_file = name+'/X_attack_test_15.csv'
    outfile = open(output_file, 'w', newline='')
    writer = csv.writer(outfile)
    for i in range(numFiles):
        file = "{0}/data_{1}.txt".format(name,i+1)
        with open(file, 'r') as f1:
            data1 = list(csv.reader(f1))
        diff = [int(data1[i+1][0])-int(data1[i][0]) for i in range(len(data1)-1)]
        writer.writerow(diff)


# Parse Arguments
########################################################################################################
# -n <value>      Name that will be used for the data collected                   Default: *timestamp*
# -r <value>      The number of times the attack will run                         Default: 4 or 15
# -w <value>      The amount of time in seconds to wait between each attack       Default: 1
# -t              Runs a test run that is not for ML model. Just for graphing     Default: False
########################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-n', '--name')
parser.add_argument('-r', '--run')
parser.add_argument('-w','--wait')
parser.add_argument('-t', '--test', action='store_true')
args = parser.parse_args()
if(args.name != None): 
    name = args.name
if(args.run != None): 
    runs = args.run
if(args.wait != None):
    wait_time = args.wait
source_file = args.filename

#########
# START #
#########
# Simply runs the attack (runs) amount of times with (wait_time) sleep between each attack
if(args.test == True):
    os.system("sh ssh_helper.sh {0} {1} {2} {3} {4} 1".format(wd,source_file,name,runs,wait_time))
    print("DATA FILE: {0}/data.txt".format(name))

# Runs the attack 15 times with 5001 data points collected for each atttac and 5s sleep between each run
else:
    if(args.run == None): 
        runs = 15
    os.system("sh ssh_helper.sh {0} {1} {2} {3} {4} 0".format(wd,source_file,name,runs,wait_time))
    processMLData(runs,name)
    os.system("sh model_helper.sh {0} {1}".format(wd,name))
    with open("{0}{1}/results.txt".format(wd,name), 'r') as f:
        print(f.read())
    print("DATA File: {0}/X_attack_test_15.csv".format(name))

