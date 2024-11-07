import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os
#new mapping_inequality data with backgroung
#https://github.com/americanpanorama/mapping-inequality-census-crosswalk
#back_end_data/mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson

##pulling the mapping_inequality data###
#and extracting only the grades
mapping = gpd.read_file("mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
#making a data that just holds the GEOID and grades for the redlined data
grades = mapping[["grade", "GEOID"]].dropna().drop_duplicates()
#dropping extra 0s from front
grades["GEOID"] = grades["GEOID"].str[1:].astype(int)
'''
#https://stackoverflow.com/questions/27965295/dropping-rows-from-dataframe-based-on-a-not-in-condition
print(grades["grade"].value_counts(normalize=True))
learned here that there are some grades that are not A,B,C,D
going to drop them because they make less than 2% of data
'''
#print(grades["grade"].value_counts(normalize=True))
grades_list = ['A','B','C','D']
grades = grades[grades['grade'].isin(grades_list)]
#print(grades["grade"].value_counts(normalize=True))
# creates a 30578 by 2 array with grade and GEOID

###FEMA###
'''
going to use every file in FEMA data to create giant dataframe
https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
'''
files = []
fema_dir = "/FEMA_data"
for fema in os.listdir(fema_dir):
    files.append(fema_dir + fema)

print(files)
colo_data = pd.read_csv("FEMA_data/NRI_Table_CensusTracts_Colorado.csv")
colo_risks = colo_data[["RISK_VALUE", "TRACTFIPS"]].dropna().drop_duplicates()

###GEOID should MAP to TRACTFIPS --> renaming each to area
grades = colorado_grades.rename(columns={"GEOID": "area"}).dropna()


risks = colo_risks.rename(columns={"TRACTFIPS": "area"})

#concated version
overall = pd.merge(grades, risks, on="area")
#print(overall['grade'])

print(overall.shape)
sns.violinplot(data=overall, x="RISK_VALUE", y="grade")

plt.show()
