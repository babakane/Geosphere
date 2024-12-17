import geopandas as gpd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

def generate_spatial_report(geodata):
    # Summary statistics
    report = {}
    report["Total Features"] = len(geodata)
    report["Geometry Types"] = geodata.geom_type.value_counts().to_dict()
    
    # Visualize dataset on a Folium map
    center = [geodata.geometry.centroid.y.mean(), geodata.geometry.centroid.x.mean()]
    m = folium.Map(location=center, zoom_start=12)
    for _, row in geodata.iterrows():
        folium.GeoJson(row["geometry"]).add_to(m)
    
    report["Map"] = m._repr_html_()
    
    return report
