import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import time

wd = os.getcwd() + "/"
source_file = sys.argv[1]
name = time.strftime("%Y%m%d-%H%M%S")
runs = 4
wait_time = 1
command = "sh grab_data_helper.sh {0} {1} {2} {3} {4}".format(wd,source_file,name,runs,wait_time)
os.system(command)

data_file = name + "/" + "data_" + name + ".txt"

print(data_file)
