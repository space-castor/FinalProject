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

fema_data = pd.read_csv(files[0])
fema_data = fema_data[["RISK_VALUE", "TRACTFIPS"]].dropna().drop_duplicates()
for index in range (1, len(files)):
    current = pd.read_csv(files[index])
    current = current[["RISK_VALUE", "TRACTFIPS"]].dropna().drop_duplicates()
    print("current is")
    print(current.shape)
    fema_data = pd.concat([fema_data, current])
    print("fema is")
    print(fema_data.shape)
print("overall is")
print(fema_data.shape)
