import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
#inequality = pd.read_json("mappinginequality.json")
#print(inequality.head())

#den_pd = pd.read_json("geojson_DEN.json")
#print(den)

print("hi")

den_gpd = gpd.read_file("mapping_inequality/geojson_DEN.json")
#print(den_gpd.columns)
'''Index(['area_id', 'city_id', 'grade', 'fill', 'label', 'name', 'category_id',
       'sheets', 'area', 'bounds', 'residential', 'commercial', 'industrial',
       'geometry'],
      dtype='object')
'''
#print(den_gpd["grade"])
'''
grade : a-d score of how desirable that area is
label: a-d score + number for area
fill: color for that area of polygone in hex
city_id: int representation of city DEN = 23
area_id: int (4 digit) representation of area, unique but not consequative
name: ?? blank for DEN
category_id: int representation of grade (1-4) + for non residential
sheets: 1.0 or 0.0 or NaN?
bounds: list of float numbers...bounds of polygone?
area: small decimal representation of area, diffent than area id how?
residential, commercial, industrial, boolean of zoneing type
geometry: list of area of multiploygone
'''
only_res = den_gpd[den_gpd['residential'] == True]
print(only_res)
sns.scatterplot(data = only_res, x = 'grade', y = 'sheets')
plt.show()
