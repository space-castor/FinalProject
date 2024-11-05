import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

#https://github.com/americanpanorama/mapping-inequality-census-crosswalk

##pullting the mapping_inequality data
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
