import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

#https://github.com/americanpanorama/mapping-inequality-census-crosswalk

##pullting the mapping_inequality data
'''
den_gpd = gpd.read_file("mapping_inequality/geojson_DEN.json")
print(den_gpd["grade"])
##pulling the FEMA data
colo_data = pd.read_csv("FEMA_data/NRI_Table_CensusTracts_Colorado.csv")
den_data = colo_data[colo_data["COUNTY"]=="Denver"]
p
risk_den_data = den_data[["RISK_VALUE", "RISK_SCORE", "RISK_RATNG"]]
print(risk_den_data)
grade_to_risk = pd.concat([risk_den_data, den_gpd["grade"]])
print(grade_to_risk)
'''
#mapping inequality
mapping = gpd.read_file("/Users/CassidyRecker/Desktop/github/FinalProject/back_end_data/mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
#print(mapping.columns)
denver_data = mapping[mapping["city"] == "Denver"]
denver_grades = denver_data[["grade", "GEOID"]].dropna().drop_duplicates()
denver_grades["GEOID"] = denver_grades["GEOID"].str[1:].astype(int)
#print(denver_grades)
#FEMA
colo_data = pd.read_csv("FEMA_data/NRI_Table_CensusTracts_Colorado.csv")
den_data = colo_data[colo_data["COUNTY"]=="Denver"]
#print(den_data.columns)
denver_risks = den_data[["RISK_VALUE", "TRACTFIPS"]].dropna().drop_duplicates()
#denver_risks.index = den_data["TRACTFIPS"]
#print(denver_risks)
###GEOID should MAP to TRACTFIPS
grades = denver_grades.rename(columns={"GEOID": "area"})
#print(grades)
risks = denver_risks.rename(columns={"TRACTFIPS": "area"})
overall = pd.merge(grades, risks, on="area")
print(overall)
