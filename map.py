import folium
import pandas

mp = folium.Map(location=[38, -99], zoom_start=6, tiles="Stamen Terrain")

fg = folium.FeatureGroup(name="Volcanoes")
fg2 = folium.FeatureGroup(name="Population")

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


def get_color(ele: float) -> str:
    if ele <= 1000:
        return 'blue'
    elif 1000 < ele <= 2000:
        return 'green'
    else:
        return 'red'


for lt, ln, el in zip(lat, lon, elev):
    fg.add_child(folium.CircleMarker(location=(lt, ln), radius=7,
                                     popup=str(el) + "m",
                                     fill_color=get_color(el), color='grey',
                                     fill_opacity=0.7))

fp = open("world.json", 'r', encoding='utf-8-sig')
fg2.add_child(folium.GeoJson(data=fp.read(), style_function=lambda x:
{'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else
 'orange' if x['properties']['POP2005'] < 20000000 else 'red'}))


mp.add_child(fg)
mp.add_child(fg2)
mp.add_child(folium.LayerControl())

mp.save("map.html")
