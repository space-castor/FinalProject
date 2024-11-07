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
values = ["RISK_VALUE", "TRACTFIPS"]
fema_dir = "FEMA_data/"
for fema in os.listdir(fema_dir):
    files.append(fema_dir + fema)

fema_data = pd.read_csv(files[0])
fema_data = fema_data[values].dropna().drop_duplicates()
for index in range (1, len(files)):
    current = pd.read_csv(files[index])
    current = current[values].dropna().drop_duplicates()
    fema_data = pd.concat([fema_data, current])


###mapping data###
values = ["grade", "GEOID"]
mapping = gpd.read_file("mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
#making a data that just holds the GEOID and grades for the redlined data
colorado_grades = mapping[values].dropna().drop_duplicates()
#dropping extra 0s from front
colorado_grades["GEOID"] = colorado_grades["GEOID"].str[1:].astype(int)
