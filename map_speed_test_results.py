import folium
from folium.plugins import FeatureGroupSubGroup
import pandas as pd
from pandas import *

map = folium.Map(location=[40.0150, -105.2705], zoom_start=4)
marker_group = folium.FeatureGroup(name='Marker Group').add_to(map)

test_results_file = "UPDATED_global_internet_speed_test_output_1746689101.842129_Manually_Cleaned.csv"
speed_test_results_data = read_csv("./script_outputs/"+str(test_results_file))
print("Read input file with ookla speed test results data: ./script_outputs/"+str(test_results_file))
test_results_df = pd.DataFrame(speed_test_results_data)
test_results_df.info()

test_results_df = test_results_df.dropna(subset=['download_speed_mbps'])
test_results_df = test_results_df.dropna(subset=['upload_speed_mbps'])

for row in test_results_df.itertuples():
    folium.Marker(
        location=[row.lat, row.lon],
        popup='serverName:'+str(row.sponsor)+'\ncountry:'+str(row.country)+'\ndown(mb/s):'+str(row.download_speed_mbps)+'\nup(mb/s):'+str(row.upload_speed_mbps),
        icon=folium.Icon()
    ).add_to(marker_group)

world_geo_data = f"world-administrative-boundaries.geojson"
folium.Choropleth(
    geo_data=world_geo_data,
    name="download speed choropleth",
    data=test_results_df,
    columns=["cc", "download_speed_mbps"],
    key_on="feature.properties.iso_3166_1_alpha_2_codes",
    fill_color="RdYlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Download Speed (mbps)",
).add_to(map)

folium.Choropleth(
    geo_data=world_geo_data,
    name="upload speed choropleth",
    data=test_results_df,
    columns=["cc", "upload_speed_mbps"],
    key_on="feature.properties.iso_3166_1_alpha_2_codes",
    fill_color="RdYlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Upload Speed (mbps)",
    show=False
).add_to(map)

folium.LayerControl(collapsed=False).add_to(map)

# Note: If you get error "ValueError: key_on `'properties.iso_3166_1_alpha_2_codes'` not found in GeoJSON." at the line below, check the key_on value in the GeoJSON file. It might contain null values which might need to be replaced with None
map.save(outfile="map.html")
