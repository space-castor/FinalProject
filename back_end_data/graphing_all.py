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
mapping_data = gpd.read_file("mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
#making a data that just holds the GEOID and grades for the redlined data
mapping_data = mapping_data[values].dropna().drop_duplicates()
#dropping extra 0s from front
mapping_data["GEOID"] = mapping_data["GEOID"].str[1:].astype(int)
#making list of grades only include grades
'''
#https://stackoverflow.com/questions/27965295/dropping-rows-from-dataframe-based-on-a-not-in-condition
print(grades["grade"].value_counts(normalize=True))
going to drop them because they make less than 2% of data
'''
grades_list = ['A','B','C','D']
mapping_data = mapping_data[mapping_data['grade'].isin(grades_list)]

###Making Concatinated version###
#making geoid and TRACTFIPS "area"
risks = fema_data.rename(columns={"TRACTFIPS": "area"})
print("risk shape")
print(risks.shape)
grades = mapping_data.rename(columns={"GEOID": "area"}).dropna()
print("grades shape")
print(grades.shape)

overall = pd.merge(grades, risks, on="area")
#print(overall['grade'])

print(overall.shape)
sns.violinplot(data=overall, x="RISK_VALUE", y="grade")

plt.show()
