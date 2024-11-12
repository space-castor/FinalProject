import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
print("start")
#def preprocess(fema_values = ["RISK_VALUE"], mapping_values = ["grades"] ):
    ###FEMA###
def preprocess():
    '''
    going to use every file in FEMA data to create giant dataframe
    https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
    '''
    files = []
    values = ["RISK_SCORE", "TRACTFIPS", "RISK_VALUE", "HWAV_RISKS", "HRCN_RISKS", "RFLD_RISKS", "TRND_RISKS", "WFIR_RISKS", "CFLD_RISKS"]
    fema_dir = "FEMA_data/"
    for fema in os.listdir(fema_dir):
        files.append(fema_dir + fema)

    fema_data = pd.read_csv(files[0])
    fema_data = fema_data[values].drop_duplicates()
    for index in range (1, len(files)):
        print("adding: ")
        print(files[index])
        current = pd.read_csv(files[index])
        current = current[values].drop_duplicates()
        fema_data = pd.concat([fema_data, current])

    print("pulled fema data")
    ###mapping data###
    print("pulling mapping data")
    values = ["grade", "GEOID", "city", "state", "geometry"]
    mapping_data = gpd.read_file("mapping_inequality/MIv3Areas_2020TractCrosswalk.geojson")
    #making a data that just holds the GEOID and grades for the redlined data
    mapping_data = mapping_data[values].dropna().drop_duplicates()
    #dropping extra 0s from front
    mapping_data["GEOID"] = mapping_data["GEOID"].astype(int)
    #making list of grades only include grades
    '''
    #https://stackoverflow.com/questions/27965295/dropping-rows-from-dataframe-based-on-a-not-in-condition
    print(grades["grade"].value_counts(normalize=True))
    going to drop them because they make less than 2% of data
    '''
    grades_list = ['A','B','C','D']
    mapping_data = mapping_data[mapping_data['grade'].isin(grades_list)]

    print("pulled mapping data")
    print("making Concatinated dataframe")
    ###Making Concatinated version###
    #making geoid and TRACTFIPS "area"
    risks = fema_data.rename(columns={"TRACTFIPS": "area"})
    print("risk shape")
    print(risks.shape)
    grades = mapping_data.rename(columns={"GEOID": "area"}).dropna()
    print("grades shape")
    print(grades.shape)

    overall = pd.merge(grades, risks, on="area")
    return overall, len(files)

def findmax(state, overall):
    '''
    makes and saves a dictionary that has info for all the states:
    includes stats for:
        N values of the plot
        type of greatest risk risk_factor
        max for each risk factor
    '''
    state_dict = {"n":0, "max" : "null", "HWAV_RISKS":0, "HRCN_RISKS":0, "RFLD_RISKS":0, "TRND_RISKS":0, "WFIR_RISKS":0, "CFLD_RISKS":0 }
    state_seperated = overall[overall["state"] == state]
    #print(state_seperated.columns)
    n = state_seperated.shape[0]
    state_dict["n"] = n
    risk_factors = ["HWAV_RISKS", "HRCN_RISKS", "RFLD_RISKS", "TRND_RISKS", "WFIR_RISKS", "CFLD_RISKS"]
    current_max = 0
    for factor in risk_factors:
        max = float(state_seperated[factor].max())
        state_dict[factor] = max
        if max > current_max:
            current_max = max
            state_dict["max"] = factor
    return state_dict

# for checking elapsed time when running in risk_by_state.py
if __name__ == "__main__":
    t0 = time.time()
    output, num_states = preprocess()
    t1= time.time()
    #print(output.head)
    print("created the data frame! It has:")
    print(output.columns)
    print("this took: ")
    print(t1-t0)

    states = output["state"].unique()
    print(num_states, len(states))
    print("states are: ")
    print(states)

    max_risks = {}
    for st in states:
        #data is a dict returing data for each state for display
        data = findmax(st, output)
        print(st)
        print(data)
        max_risks[st] = data
    #print(max_risks)
