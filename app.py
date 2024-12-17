import streamlit as st
import geopandas as gpd
from analysis_engine import process_file, perform_spatial_analysis
from spatial_report import generate_spatial_report
import sqlite3
from folium import Map

# Initialize SQLite database
DATABASE = "database/geosphere.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''CREATE TABLE IF NOT EXISTS uploads
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     file_name TEXT, file_type TEXT, upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.close()

# Streamlit App UI
def main():
    st.title("GeoSphere: Interactive Spatial Analysis Tool")
    st.sidebar.header("Upload and Analyze Spatial Files")
    option = st.sidebar.selectbox("Select Analysis Type", ["Spatial Report", "General Spatial Analysis"])
    
    # Upload section
    uploaded_file = st.sidebar.file_uploader("Upload a Spatial File", type=["geojson", "json", "tif", "shp"])
    
    if uploaded_file:
        # Save file locally
        with open(f"data/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Add to database
        conn = sqlite3.connect(DATABASE)
        conn.execute("INSERT INTO uploads (file_name, file_type) VALUES (?, ?)", (uploaded_file.name, uploaded_file.type))
        conn.commit()
        conn.close()
        
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        # Process file
        geodata = process_file(f"data/{uploaded_file.name}")
        
        if option == "Spatial Report":
            st.subheader("Spatial Report")
            report = generate_spatial_report(geodata)
            st.write(report)
        
        elif option == "General Spatial Analysis":
            st.subheader("General Spatial Analysis")
            analysis_result = perform_spatial_analysis(geodata)
            st.write(analysis_result)

if __name__ == "__main__":
    init_db()
    main()
