import streamlit as st
import pandas as pd
st.title("Dashboard View")
def map_view():
    UNI_LAT=34.0691 
    UNI_LON= 72.6441
    map_data = pd.DataFrame(
    {'lat': [UNI_LAT], 'lon': [UNI_LON]}
            
                )
    st.map(map_data)
    df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
    })
# write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))
map_view()
