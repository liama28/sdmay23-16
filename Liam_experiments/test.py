import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import time
import matlab.engine

eng = matlab.engine.start_matlab()

eng.graph_raw_power_data("{0}/20221109-171950/data_20221109-171950.txt".format(os.getcwd()))

eng.quit()
