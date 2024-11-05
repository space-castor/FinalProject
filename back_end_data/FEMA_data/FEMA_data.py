import pandas as pd
import numpy as np

colo_data = pd.read_csv("NRI_Table_CensusTracts_Colorado.csv")
den_data = colo_data[colo_data["COUNTY"]=="Denver"]

risk_den_data = den_data[["RISK_VALUE", "RISK_SCORE", "RISK_RATNG"]]

print(risk_den_data)
