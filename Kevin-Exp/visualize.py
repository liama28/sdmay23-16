# To run, do visualize.py [datafilenamehere.txt]
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

# x, y = np.loadtxt('output.txt', delimiter = ',', unpack=True)

x = []
y = []

with open(sys.argv[1], 'r') as data:
	plot = csv.reader(data, delimiter=',')

	diff = 0
	priorVal = 0
	
	for rows in plot:
		if priorVal == 0:
			priorVal = int(rows[1])
			next(plot)
		else:
			x.append(int(rows[0]))
			diff = int(rows[1]) - priorVal
			y.append(diff)
			priorVal = int(rows[1])

plt.plot(x,y)
plt.title('Power Consumption')
plt.xlabel('Points')
plt.ylabel('Power')
plt.show()
