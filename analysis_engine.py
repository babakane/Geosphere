import geopandas as gpd
from shapely.geometry import Point
import numpy as np

def process_file(file_path):
    """Process the uploaded file and return a GeoDataFrame."""
    try:
        geodata = gpd.read_file(file_path)
        return geodata
    except Exception as e:
        return str(e)

def perform_spatial_analysis(geodata):
    """Perform various spatial analyses on the GeoDataFrame."""
    results = {}
    
    # Example: Calculate centroids
    geodata["centroid"] = geodata.geometry.centroid
    
    # Example: Spatial buffer
    geodata["buffer"] = geodata.geometry.buffer(0.01)  # 0.01 degrees buffer
    
    # Example: Calculate bounding box
    bounds = geodata.total_bounds
    results["Bounding Box"] = {"min_x": bounds[0], "min_y": bounds[1], "max_x": bounds[2], "max_y": bounds[3]}
    
    # Example: Clustering using spatial proximity
    from sklearn.cluster import DBSCAN
    coords = np.array(list(zip(geodata.centroid.x, geodata.centroid.y)))
    clustering = DBSCAN(eps=0.1, min_samples=2).fit(coords)
    geodata["cluster"] = clustering.labels_
    results["Clustering"] = geodata[["centroid", "cluster"]].to_dict("records")
    
    return results
