import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time


def fema_df():
    '''
    going to use every file in FEMA data to create giant dataframe
    https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
    '''
    files = []
    #"CWAV_RISKS", "HWAV_RISKS", "HRCN_RISKS", "RFLD_RISKS", "TRND_RISKS", "WFIR_RISKS"
    values = ["RISK_SCORE", "TRACTFIPS"]
    fema_dir = "FEMA_data/"
    for fema in os.listdir(fema_dir):
        files.append(fema_dir + fema)

    fema_data = pd.read_csv(files[0])
    fema_data = fema_data[values].dropna().drop_duplicates()
    for index in range (1, len(files)):
        print("adding: ")
        print(files[index])
        current = pd.read_csv(files[index])
        current = current[values].dropna().drop_duplicates()
        fema_data = pd.concat([fema_data, current])
    return fema_data

def mapping_df():
    values = ["grade", "GEOID", "city", "state", "geometry"]
    mapping_data = gpd.read_file("mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
    #making a data that just holds the GEOID and grades for the redlined data
    mapping_data = mapping_data[values].dropna().drop_duplicates()
    mapping_data["GEOID"] = mapping_data["GEOID"].astype(int)

    grades_list = ['A','B','C','D']
    mapping_data = mapping_data[mapping_data['grade'].isin(grades_list)]
    return mapping_data


#def preprocess(fema_values = ["RISK_VALUE"], mapping_values = ["grades"] ):
    ###FEMA###
def preprocess(fema_data, mapping_data):

    risks = fema_data.rename(columns={"TRACTFIPS": "area"})
    print("risk shape")
    print(risks)
    grades = mapping_data.rename(columns={"GEOID": "area"}).dropna()
    print("grades shape")
    print(grades)

    overall = pd.merge(grades, risks, on="area")
    return overall

t0 = time.time()
output = preprocess(fema_df(), mapping_df())
t1= time.time()
pd.set_option("display.max_rows", None)

#print(output.head)
#print(output.columns)

#print(output["state"])
print(t1-t0)
