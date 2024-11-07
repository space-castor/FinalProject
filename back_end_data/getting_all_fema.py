import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os

###FEMA###
'''
going to use every file in FEMA data to create giant dataframe
https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
'''
files = []
fema_dir = "FEMA_data/"
for fema in os.listdir(fema_dir):
    files.append(fema_dir + fema)

print(files)
print(len(files))
