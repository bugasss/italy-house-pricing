import streamlit as st
import pandas as pd
import numpy as np
import os
import streamlit as st
import geopandas as gpd
import pandas as pd
import urllib
import folium
from IPython.display import display

from matplotlib import pyplot as plt
#url = 'https://github.com/napo/geospatial_course_unitn/raw/master/data/istat/istat_administrative_units_generalized_2022.gpkg'
#urllib.request.urlretrieve(url ,"istat_administrative_units_generalized_2022.gpkg")
import warnings
warnings.filterwarnings('ignore')

jsn = "data/limits_IT_regions.geojson"

m = folium.Map(location=[41.87194, 12.56738],
               zoom_start=6,
               tiles='cartodbpositron',
               name='Italy')

#comuni = pd.read_excel('data/comuni.xlsx')
#comuni.rename(columns={'Denominazione in italiano': 'citta'}, inplace=True)
#df = pd.merge(df, comuni, on='citta', how='left')

#%%
st.set_page_config(page_title='Dashboard', layout='wide')

st.title("ITALY HOUSING PRICES")

st.sidebar.title('About')
st.sidebar.info('Explore the Highway Statistics')


df = pd.read_parquet("italy_housing_price_rent_raw.parquet.gzip")
df = df.dropna(subset=['regione'])

#%%
folium.Choropleth(
    geo_data=jsn,
    name='choropleth',
    data=df,
    columns=['regione', 'prezzo']
).add_to(m)
folium.features.GeoJson(jsn,
                        name='regions').add_to(m)
italy_coords = (41.87, 12.56)
myMap = folium.Map(location=italy_coords, zoom_start=12)
display(myMap)


#%%
m = folium.Map(location=[41.87194, 12.56738],
               zoom_start=6,
               name='Italy')
m
#%%
