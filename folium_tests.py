import geopandas
import folium

gjf = geopandas.read_file("mappinginequality.json")
#print(gjf)

testmap = folium.Map(tiles="cartodb positron")
#testmap = folium.Map(tiles="stamenterrain", attr="test")
#tileset = 'https://{s}.tile.thunderforest.com/neighbourhood/{z}/{x}/{y}.png?apikey={apikey}'
#copyline = '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
#testmap = folium.Map(tiles=tileset, attr=copyline)

redlining_data = "mappinginequality.json"

# print(gjf["grade"])
for i in range( len( gjf["geometry"] ) ):
    zone = gjf["geometry"][i]
    grade_color = gjf["fill"][i]
    city = gjf["city"][i]
    grade = gjf["grade"][i]
    category = gjf["category"][i]

    #Playing with popups - ugly but works!
    try:
        text = ("City: " + city + "\nGrade: " + grade + "\nCategory: " + category)
    except:
        text = ("City: " + city + "\nGrade: not available")

    popup = folium.Popup(text, lazy = True)

    #Hovering stuffs
    try:
        hover_txt = ("\nCategory: " + category)
    except:
        hover_txt = ("Category not available")

    tooltip = folium.Tooltip(hover_txt)

    folium.GeoJson(zone, color=grade_color, weight=1, fill_opacity=0.5, popup = popup, tooltip = tooltip).add_to(testmap)

#for i in range( len( gjf["geometry"] ) ):
#    if gjf["city"][i] == "Colorado Springs":
#        print(gjf.loc[i])

testmap.fit_bounds( [(25,-125), (50,-70)] )
testmap.save("test_map.html")
