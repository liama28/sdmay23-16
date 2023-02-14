import argparse
import sys
import os
import time
import csv

wd = os.getcwd() + "/"
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
source_file = args.filename

output_file = 'X_attack_test_15.csv'
outfile = open(output_file, 'w', newline='')
writer = csv.writer(outfile)
file = source_file
f1 = open(file, 'r')
data = list(csv.reader(f1))
for i in range(15):
    diff = [int(data[i*5001+j+1][0])-int(data[i*5001+j][0]) for j in range(5000)]
    writer.writerow(diff)