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
runs = 5
# The wait time between runs
wait_time = 0.2

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
# -r <value>      The number of times the attack will run                         Default: 5 or 15
# -w <value>      The amount of time in seconds to wait between each attack       Default: 0.2
# -t              Runs a test run that is not for ML model. Just for graphing     Default: False
# -s              Skips running the data on the ML model                          Default: False
# -p              Profiles provided x86 instructions                              Default: False
########################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-n', '--name')
parser.add_argument('-r', '--run')
parser.add_argument('-w','--wait')
parser.add_argument('-s', '--skip', action='store_true')
parser.add_argument('-t', '--test', action='store_true')
parser.add_argument('-p', '--profile', action='store_true')
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

# ______________________________________________________________________________________________________

# Simply runs the attack (runs) amount of times with (wait_time) sleep between each attack
if(args.test == True):
    os.system("sh ssh_helper.sh {0} {1} {2} {3} {4} 1".format(wd,source_file,name,runs,wait_time))
    print("DATA FILE: {0}/data.txt".format(name))

# ______________________________________________________________________________________________________

elif(args.profile == True):
    os.system("sh ssh_helper.sh {0} {1} {2} {3} {4} 2".format(wd,source_file,name,runs,wait_time))

    # Timing
    with open("{0}{1}/time.txt".format(wd,name)) as f:
        lines = f.readlines()
    total, count = 0, 0
    for line in lines:
        fields = line.split()
        value = float(fields[1])
        print(f"Run time: {value}")
        total += value
        count += 1
    averageTime = total / count
    numInstructions = lines[0].split()[0]

    # Data
    with open("{0}{1}/data.txt".format(wd,name)) as f:
        data = [int(line.strip()) for line in f.readlines()]
    data_new = [data[i+1] - data[i] for i in range(len(data)-1)]

    # Average power value
    with open("{0}{1}/int.txt".format(wd,name)) as f:
        interruptData = [int(line.strip()) for line in f.readlines()]
    ranges = [(interruptData[i], interruptData[i+1]) for i in range(0, len(interruptData), 2)]
    total, count = 0, 0
    totalSamples = 0
    for start, end in ranges:
        if start < 0 or end > len(data_new) or start >= end:
            print(f"Invalid range ({start}, {end})")
        else:
            totalSamples += end - start
            average = sum(data_new[start:end]) / ((end-start))
            total += average
            count += 1
            print(f"Average value for range ({start}, {end}): {average}")
    averagePower = total / count


    # Stats
    print("\nStats:\n___________")
    print("Average time: {} ms".format(averageTime))
    print("Number of instructions: {} million".format(numInstructions))
    print("Average power value: {}".format(averagePower))
    print("Average number of power values: {}".format(totalSamples))
    print("DATA FILE: {0}/data.txt".format(name))

# ______________________________________________________________________________________________________

# Runs the attack 15 times with 5001 data points collected for each atttac and 5s sleep between each run
else:
    if(args.run == None): 
        runs = 15
    os.system("sh ssh_helper.sh {0} {1} {2} {3} {4} 0".format(wd,source_file,name,runs,wait_time))
    processMLData(runs,name)
    if not args.skip:
        os.system("sh model_helper.sh {0} {1}".format(wd,name))
        with open("{0}{1}/results.txt".format(wd,name), 'r') as f:
            print(f.read())
    print("DATA File: {0}/X_attack_test_15.csv".format(name))

# ______________________________________________________________________________________________________

