import geopandas
import folium
import branca
from overall_dataframeV2 import *

# pulls method to create the dataframe from overall_dataframeV2 to be accessible to this file
data = preprocess(fema_df(), mapping_df())

print(data.head())

base = folium.Map(tiles="cartodb positron")

# referenced from foliums user guide on geojson popups and tooltips
colormap = branca.colormap.LinearColormap(
    vmin=data["RISK_SCORE"].quantile(0.0),
    vmax=data["RISK_SCORE"].quantile(1),
    colors=["red", "orange", "lightblue", "green", "darkgreen"],
    caption= "Areas Climate Risk Score",
)

g = folium.GeoJson(
    data,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["RISK_SCORE"])
        """if x["properties"]["RISK_SCORE"] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,"""
    }
).add_to(base)

base.fit_bounds( [(25,-125), (50,-70)] )
base.save("base_map.html")
