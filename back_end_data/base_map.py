import geopandas as gpd
import folium
import branca
import requests
import io
from overall import *
from jinja2 import Template

# MAIN DATA FILE
# pulls method to create the dataframe from risk_by_state to be accessible to this file
overall, num_states  = preprocess()

base = folium.Map([43, -100], zoom_start=4)

# COLOR FUNCTIONS

# sets up a color dictionary associated with the different scores
# referenced from foliums user guide on geojson popups and tooltips

# state level color functions
climate_map = branca.colormap.LinearColormap(
    vmin=overall["RISK_SCORE"].quantile(0.0),
    vmax=overall["RISK_SCORE"].quantile(1),
    colors=["yellow", "orange", "red"],
    caption= "Areas Climate Risk Score",
)

def color_grade (value):
    colorlist = ["#b3c7f7", "#8babf1", "#0073e6", "#054fb9"]
    if value == "A":
        return colorlist[0]
    elif value == "B":
        return colorlist[1]
    elif value == "C" :
        return colorlist[2]
    elif value == "D":
        return colorlist[3]
    else:
        return "white"

# country view color function
def color_risk(value):  # scalar value defined in 'column'
    colorlist = ["#00bf7d", "#00b4c5", "#8dd2dd", "#0073e6", "#2546f0", "#5928ed"]
    if value == "HWAV_RISKS":
        return colorlist[0]
    elif value == "HRCN_RISKS":
        return colorlist[1]
    elif value == "CFLD_RISKS" :
        return colorlist[2]
    elif value == "RFLD_RISKS":
        return colorlist[3]
    elif value == "TRND_RISKS":
        return colorlist[4]
    elif value == "WFIR_RISKS" :
        return colorlist[5]
    else:
        return "white"

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
    state_dict["name"] = st
    index = list(states_plot["name"].keys())[list(states_plot["name"].values()).index(abbr[st])]
    state_dict["geometry"] = states_plot["geometry"][index]
    cv_df.append(state_dict)
    img = makeplot(st, "RISK_SCORE", overall)
    state_dict["image"] = img

# reconvert into data frame
cv_df = gpd.GeoDataFrame(cv_df, crs="EPSG:4326")

# Country Map Set Up
for i in range(len(cv_df["name"])):
    zone = cv_df["geometry"][i]
    risk_color = color_risk(cv_df["max"][i])

    # tooltip set up
    fields=["name", "n", "max" , "HWAV_RISKS", "HRCN_RISKS", "RFLD_RISKS",
        "TRND_RISKS", "WFIR_RISKS", "CFLD_RISKS"]
    aliases=["State: ", "Number of areas recorded: ", "Highest Risk: ", "Heatwave Risk: ", "Hurricane Risk:",
        "Rainflood Risk: ", "Tornado Risk: ", "Wildfire Risk: ", "Coastal Flooding Risk: "]
    tooltip_text = "\n" + str([aliases[x] + str(cv_df[fields[x]][i]) + "\n" for x in range(len(fields))])

    img = cv_df["image"][i]
    html_string = "hello"
   #f"<img src = {{img}} alt= "State violin plot">"

    popup = folium.Popup(html_string, lazy = True)

    tooltip = folium.Tooltip(
        tooltip_text,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """)

    tooltip = folium.Tooltip(tooltip_text)

    folium.GeoJson(zone, color=risk_color, weight=1, fill_opacity=0.5, popup = popup, tooltip = tooltip).add_to(base)
''''
country_view = folium.GeoJson(
    cv_df,
    style_function = lambda feature: {
        "fillColor": color_risk(feature["properties"]["max"]),
        "fillOpacity": 0.5,
    },
    tooltip = tooltip
).add_to(base)
'''
'''
# as prettu as this is, this is not compatible with branca elements so
base = cv_df.explore(
    column = "max",  # make choropleth based on "max" column
    scheme = "Quantiles",
    cmap = "Blues",
    legend=True,  # show legend
    popup= False,  # show popup (on-click)
    marker_type = folium.Marker(),
#    legend_kwds=dict(colorbar=False),  # do not use colorbar
    name="country_view",  # name of the layer in the map
)
climate_map.add_to(base)
'''

# --------- STATE LEVEL -----------
# personalized ->  generated at the user input

#  function to only pull up state data
def pull(state, state_list):
    try:
        if state in state_list:
            raise IndexError

        tooltip = folium.GeoJsonTooltip(
            fields=["state", "city", "RISK_SCORE", "grade", "category"],
            aliases=["State:", "City:", "Risk Score:", "Grade:", "Category:"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )

        popup = folium.GeoJsonTooltip(
            fields=["state", "city", "RISK_SCORE", "grade", "category", "HWAV_RISKS", "HRCN_RISKS", "RFLD_RISKS",
                "TRND_RISKS", "WFIR_RISKS", "CFLD_RISKS"],
            aliases=["State:", "City:", "Risk Score:", "Grade:", "Category:", "Heatwave Risk:", "Hurricane Risk:",
                "Rainflood Risk:", "Tornado Risk:", "Wildfire Risk:", "Coastal Flooding Risk:"],
            localize=True,
            sticky= True,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
            lazy = True,
        )

        # climate change layer
        new_state = folium.GeoJson(
            overall[(overall["state"] == state)],
            style_function=lambda x: {
                "fillColor": climate_map(x["properties"]["RISK_SCORE"])
                if x["properties"]["RISK_SCORE"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.4,
            },
            control = True,
            smooth_factor = 1.0,
            name = state + "-climate-risk",
            zoom_on_click = True,
            tooltip = tooltip,
            popup = popup
        ).add_to(base)

        # red-lining layer
        new_state = folium.GeoJson(
            overall[(overall["state"] == state)],
            style_function=lambda x: {
                "fillColor": color_grade(x["properties"]["grade"])
                if x["properties"]["grade"] is not None
                else "transparent",
                "color": "black",
                "fillOpacity": 0.4,
            },
            control = True,
            smooth_factor = 1.0,
            name = state + "-redlining",
            zoom_on_click = True,
            tooltip = tooltip,
            popup = popup
        ).add_to(base)


    except IndexError:
        print(state + " has already been added to your map.")
    except:
        print("We do not have " + state + " as a valid state abbreviations.")


'''
city_risks = overall.groupby(["city"], as_index = False)["RISK_SCORE"].mean()
disolved_city = overall.dissolve(by = ["state", "city"], method = "unary")

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
            print("Done!")

        if action == "see":
            print("The following states added are : " +  str(states))

        if action == "export":
            file_name = input("Okay! What would you like to name your file? ")
            folium.LayerControl().add_to(base)  # use folium to add layer control
            base.save((file_name + ".html"))
            print("Done!")

        # not an infinite loop!
        if action == "quit":
            done = True
            print("Okay! Thanks, come again later!")

# --- Actually running the code -------

print("Alrighty! We're ready for you!")
userInteract()
