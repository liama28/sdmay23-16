import argparse
import sys
import os
import time
import csv

# Default Values
wd = os.getcwd() + "/"
#source_file = sys.argv[1]
name = time.strftime("%Y%m%d-%H%M%S")
runs = 4
wait_time = 1
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


# Parse Arguments
########################################################################################################
# -n <value>      Name that will be used for the data collected                   Default: *timestamp*
# -r <value>      The number of times the attack will run                         Default: 4
# -w <value>      The amount of time in seconds to wait between each attack       Default: 1
# -m              Runs power signature collection for the ML Model                Default: False
########################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-n', '--name')
parser.add_argument('-r', '--run')
parser.add_argument('-w','--wait')
parser.add_argument('-m', '--model', action='store_true')
args = parser.parse_args()
if(args.name != None): 
    name = args.name
if(args.run != None): 
    runs = args.run
if(args.wait != None):
    wait_time = args.wait
source_file = args.filename

# Grab data for the machine learning model
if(args.model == True):
    if(args.run == None): 
        runs = 30
    command = "sh scp_helper.sh {0} {1} {2} {3} {4} 1".format(wd,source_file,name,runs,wait_time)
    os.system(command)
    processMLData(runs,name)

# Simply run attack # amount of times with # seconds between each attack
else:
    command = "sh scp_helper.sh {0} {1} {2} {3} {4} 0".format(wd,source_file,name,runs,wait_time)
    os.system(command)
    data_file = name + "/" + "data_" + name + ".txt"
    print("DATA FILE: {0}".format(data_file))
