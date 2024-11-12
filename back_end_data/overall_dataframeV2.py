import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time


def fema_df():
    '''
    going to loop through every FEMA data csv file to create giant dataframe
    https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
    '''
    files = []

    # making a dataframe that just holds the tractfips, composite risk score,
    # and selected natural hazard risk scores for the fema data
    values = ["RISK_SCORE", "TRACTFIPS", "CFLD_RISKS", "HWAV_RISKS", "HRCN_RISKS",
        "RFLD_RISKS", "TRND_RISKS", "WFIR_RISKS"]
    fema_dir = "FEMA_data/"

    # making a list of all of the FEMA files
    for fema in os.listdir(fema_dir):
        files.append(fema_dir + fema)

    fema_data = pd.read_csv(files[0])
    fema_data = fema_data[values].dropna().drop_duplicates()

    # using pandas to pull wanted data from every file
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

    # making a dataframe that just holds the GEOID, grades, city, state, and geometry
    # for the redlined data
    mapping_data = mapping_data[values].dropna().drop_duplicates()
    mapping_data["GEOID"] = mapping_data["GEOID"].astype(int)

    '''
    #https://stackoverflow.com/questions/27965295/dropping-rows-from-dataframe-based-on-a-not-in-condition
    print(mapping_data["grade"].value_counts(normalize=True))
    going to drop them because they make less than 4% of data'''

    grades_list = ['A','B','C','D']
    mapping_data = mapping_data[mapping_data['grade'].isin(grades_list)]
    return mapping_data



def preprocess(fema_data, mapping_data):
    # changing column titles for TRACTFIPS and GEOID in order to concatinate
    risks = fema_data.rename(columns={"TRACTFIPS": "area"})

    grades = mapping_data.rename(columns={"GEOID": "area"}).dropna()

    # concatinating both datasets on area column
    overall = pd.merge(grades, risks, on="area")
    return overall



t0 = time.time()
output = preprocess(fema_df(), mapping_df())
print(output)
t1= time.time()
pd.set_option("display.max_rows", None)

#print(output.head)
#print(output.columns)

#print(output["state"])
print(t1-t0)
