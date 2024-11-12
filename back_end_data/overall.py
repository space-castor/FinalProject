import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

print("start")

    ###FEMA###
def preprocess():
    ''' cleaning and organizing mapping inequality data and FEMA data into
    overall dataframe

    going to use every file in FEMA data to create giant dataframe
    https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
    '''

    files = []

    # making a dataframe that just holds the tractfips, composite risk score,
    # and selected natural hazard risk scores for the fema data
    values = ["RISK_SCORE", "TRACTFIPS", "RISK_VALUE", "HWAV_RISKS", "HRCN_RISKS", "RFLD_RISKS", "TRND_RISKS", "WFIR_RISKS", "CFLD_RISKS"]
    fema_dir = "FEMA_data/"

    # making a list of all of the FEMA files
    for fema in os.listdir(fema_dir):
        files.append(fema_dir + fema)

    fema_data = pd.read_csv(files[0])
    fema_data = fema_data[values].drop_duplicates()

    # using pandas to pull wanted data from every file
    for index in range (1, len(files)):
        print("adding: ")
        print(files[index])
        current = pd.read_csv(files[index])
        current = current[values].drop_duplicates()
        fema_data = pd.concat([fema_data, current])

    print("pulled fema data")
    ###mapping data###


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

    print("pulled mapping data")
    ###Making Concatinated version###
    #making geoid and TRACTFIPS "area"
    risks = fema_data.rename(columns={"TRACTFIPS": "area"})

    grades = mapping_data.rename(columns={"GEOID": "area"}).dropna()

    # concatinating both datasets on area column
    overall = pd.merge(grades, risks, on="area")
    return overall, len(files)

def makeplot(state, risk_factor, overall):
    '''
    makes and saves a violin plot for the inputed state
    includes stats for:
        range of risk
        N values of the plot
    '''

    state_seperated = overall[overall["state"] == state]

    n = state_seperated.shape[0]
    max = state_seperated[risk_factor].max()
    min = state_seperated[risk_factor].min()
    print(state,n,min,max)
    # creating and saving the plot
    curr = sns.violinplot(data=state_seperated, x=risk_factor, y="grade")
    figname = "state_violin_plots/" + state + "_V_" + risk_factor + ".png"
    curr.figure.savefig(figname)
    plt.clf()

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

# for checking elapsed time when running in overall.py
if __name__ == "__main__":
    t0 = time.time()
    output, num_states = preprocess()
    t1= time.time()

    print("created the data frame! It has:")
    print(output.columns)
    print("this took: ")
    print(t1-t0)

    # creates output to understand how many states got dropped from the dataset
    states = output["state"].unique()
    print(num_states, len(states))
    print("states are: ")
    print(states)

    # dictionary that hold risk information for each state as well as
    # the number of data points for each state
    max_risks = {}
    for st in states:
        print(st)
        makeplot(st, "RISK_SCORE", output)
        #data is a dict returing data for each state for display
        data = findmax(st, output)
        print(data)
        max_risks[st] = data
