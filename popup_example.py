## BASE EXAMPLE TAKEN FROM DOCUMENTATION
import pandas as pd
import geopandas
import requests
import io
import folium
import branca


income = pd.read_csv(
    "https://raw.githubusercontent.com/pri-data/50-states/master/data/income-counties-states-national.csv",
    dtype={"fips": str},
)
income["income-2015"] = pd.to_numeric(income["income-2015"], errors="coerce")

#print(income.head())

data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()

states = geopandas.GeoDataFrame.from_features(data, crs="EPSG:4326")

# print(states.head())

response = requests.get(
    "https://gist.githubusercontent.com/tvpmb/4734703/raw/"
    "b54d03154c339ed3047c66fefcece4727dfc931a/US%2520State%2520List"
)
abbrs = pd.read_json(io.StringIO(response.text))

# print(abbrs.head(3))

statesmerge = states.merge(abbrs, how="left", left_on="name", right_on="name")
statesmerge["geometry"] = statesmerge.geometry.simplify(0.05)

statesmerge["medianincome"] = statesmerge.merge(
    income.groupby("state")["income-2015"].median(),
    how="left",
    left_on="alpha-2",
    right_on="state",
)["income-2015"]
statesmerge["change"] = statesmerge.merge(
    income.groupby("state")["change"].median(),
    how="left",
    left_on="alpha-2",
    right_on="state",
)["change"]


colormap = branca.colormap.LinearColormap(
    vmin=statesmerge["change"].quantile(0.0),
    vmax=statesmerge["change"].quantile(1),
    colors=["red", "orange", "lightblue", "green", "darkgreen"],
    caption="State Level Median County Household Income (%)",
)

m = folium.Map(location=[35.3, -97.6], zoom_start=4)

popup = folium.GeoJsonPopup(
    fields=["name", "change"],
    aliases=["State", "% Change"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

tooltip = folium.GeoJsonTooltip(
    fields=["name", "medianincome", "change"],
    aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
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


g = folium.GeoJson(
    statesmerge,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["change"])
        if x["properties"]["change"] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,
    },
    tooltip=tooltip,
    popup=popup,
).add_to(m)

colormap.add_to(m)

m.save("index.html")
