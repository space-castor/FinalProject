import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
#new mapping_inequality data with backgroung
#https://github.com/americanpanorama/mapping-inequality-census-crosswalk
#back_end_data/mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson

##pulling the mapping_inequality data###
#mapping inequality
mapping = gpd.read_file("/Users/CassidyRecker/Desktop/github/FinalProject/back_end_data/mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
#making a data that just holds the GEOID and grades for the redlined data
denver_data = mapping[mapping["city"] == "Denver"]
denver_grades = denver_data[["grade", "GEOID"]].dropna().drop_duplicates()
#dropping extra 0s from front
denver_grades["GEOID"] = denver_grades["GEOID"].str[1:].astype(int)

#FEMA###
colo_data = pd.read_csv("FEMA_data/NRI_Table_CensusTracts_Colorado.csv")
den_data = colo_data[colo_data["COUNTY"]=="Denver"]
denver_risks = den_data[["RISK_VALUE", "TRACTFIPS"]].dropna().drop_duplicates()

###GEOID should MAP to TRACTFIPS --> renaming each to area
grades = denver_grades.rename(columns={"GEOID": "area"})
risks = denver_risks.rename(columns={"TRACTFIPS": "area"})
#concated version
overall = pd.merge(grades, risks, on="area")

sns.violinplot(data=overall, x="RISK_VALUE", y="grade")

plt.show()
