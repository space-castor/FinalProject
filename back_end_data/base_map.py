import geopandas as gpd
import folium
import branca
import requests
import io
from risk_by_state import *

# MAIN DATA FILE
# pulls method to create the dataframe from risk_by_state to be accessible to this file
overall, num_states  = preprocess()

# COLOR FUNCTIONS / DICTIONARIES

# sets up a color dictionary associated with the different scores
# referenced from foliums user guide on geojson popups and tooltips
climate_map = branca.colormap.LinearColormap(
    vmin=overall["RISK_SCORE"].quantile(0.0),
    vmax=overall["RISK_SCORE"].quantile(1),
    colors=["orange", "yellow", "lightblue", "blue"],
    caption= "Areas Climate Risk Score",
)

'''
def color_risk(value):  # scalar value defined in 'column'
    if value == "HWAV_RISKS":
        return "#00bf7d"
    elif value == "HRCN_RISKS":
        return "#00b4c5"
    elif value == "CFLD_RISKS" :
        return "#8dd2dd"
    elif value == "RFLD_RISKS":
        return "#0073e6"
    elif value == "TRND_RISKS":
        return "#2546f0"
    elif value == "WFIR_RISKS" :
        return "#5928ed"
    else:
        return "white"
'''

# GEOMETRY / TRANSLATION RESOURCES

# map of the main us states - referenced from folium's user guide
refer = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
states_plot = gpd.GeoDataFrame.from_features(refer, crs="EPSG:4326").to_dict()

# translate state abbreviations of overall dataframe to state names for state geography dataframe
abbr = {
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States.
    "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona", "CA": "California",
    "CO": "Colorado","CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine",
    "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri", "MS": "Mississippi", "MT": "Montana",
    "NC": "North Carolina", "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia", "VT": "Vermont",
    "WA": "Washington", "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming"
}

# --------- COUNTRY LEVEL -----------
# individual states highlighted - generalized entire country

# since not every state is in the dataframe, this felt the most intuitive to me to prevent errors
cv_df = []
state_list = overall["state"].unique()
for st in state_list:
    #overall is a dict returing data for each state for display
    state_dict = findmax(st, overall)
    index = list(states_plot["name"].keys())[list(states_plot["name"].values()).index(abbr[st])]
    state_dict["geometry"] = states_plot["geometry"][index]
    cv_df.append(state_dict)

# reconvert into data frame
cv_df = gpd.GeoDataFrame(cv_df, crs="EPSG:4326")

# Base Map Set Up / Country Level Information
base = cv_df.explore(
    column = "max",  # make choropleth based on "max" column
    scheme = "Quantiles",
    cmap = "Blues",
    legend=True,  # show legend
    popup= False,  # show popup (on-click)
    # marker_type = folium.Marker(),
#    legend_kwds=dict(colorbar=False),  # do not use colorbar
    name="country_view",  # name of the layer in the map
)
climate_map.add_to(base)

# --------- STATE LEVEL -----------
# personalized ->  generated at the user input
# temporary function to only pull up state data -> to be replaced with preprocess method with state parameter
def pull(state, state_list):
    try:
        if state in state_list:
            raise IndexError
        new_state = folium.GeoJson(
            overall[(overall["state"] == state)],
            style_function=lambda x: {
                "fillColor": climate_map(x["properties"]["RISK_SCORE"])
                if x["properties"]["RISK_SCORE"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.7,
            },
            control = True,
            smooth_factor = 1.0,
            name = state,
            zoom_on_click = True
        ).add_to(base)
    except IndexError:
        print(state + " has already been added to your map.")
    except:
        print("We do not have " + state + " as a valid state abbreviations.")


'''
# ---- STATE LEVEL --------
city_risks = overall.groupby(["city"], as_index = False)["RISK_SCORE"].mean()
disolved_city = overall.dissolve(by = ["state", "city"], method = "unary")

g = folium.GeoJson(
    statesmerge,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["RISK_SCORE"])
        if x["properties"]["RISK_SCORE"] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,
    }
).add_to(base)
'''
""" processing everything
g = folium.GeoJson(
    overall,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["RISK_SCORE"])
        if x["properties"]["RISK_SCORE"] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,
    }
).add_to(base)"""

base.fit_bounds( [(25,-125), (50,-70)] )
folium.TileLayer("CartoDB positron", show=False).add_to(
    base
)  # use folium to add alternative tiles
'''
folium.LayerControl().add_to(base)  # use folium to add layer control
'''
# --------- USER INTERACTION ----------

def help():
    print("This program will create and export a map with informaiton analyzing the connection between redlining and climate impact.")
    print("\t'add': add a new state")
    print("\t'see': see all states added")
    print("\t'export': view map as html file")
    print("\t'quit': exit the program\n")

def userInteract():
    states = []
    # variable to keep track of whether we're finished
    done = False

    while not done:
    # prompt user for what action they would like to take
        action = input("What action would you like to take? ('help' for options): ")

        if action == "help":
            help()

        if action == "add":
            state = input("Okay! What state would you like to add? (abbreviations please!) ")
            pull(state, states)
            states.append(state)

        if action == "see":
            print("The following states added are : " +  str(states))

        if action == "export":
            file_name = input("Okay! What would you like to name your file? ")
            folium.LayerControl().add_to(base)  # use folium to add layer control
            base.save((file_name + ".html"))

        # not an infinite loop!
        if action == "quit":
            done = True
            print("Okay! Thanks, come again later!")

# --- Actually running the code -------

print("Alrighty! We're ready for you!")
userInteract()
