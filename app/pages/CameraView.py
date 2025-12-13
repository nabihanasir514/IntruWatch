UNI_LAT=34.0691 
UNI_LON= 72.6441
map_data = pd.DataFrame(
{'lat': [UNI_LAT], 'lon': [UNI_LON]}
        
            )
st.map(map_data)