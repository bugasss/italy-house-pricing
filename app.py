import streamlit as st
import pandas as pd
import numpy as np
import os
import streamlit as st
import geopandas as gpd
import pandas as pd
import urllib
import folium
from streamlit_folium import st_folium
from IPython.display import display

from matplotlib import pyplot as plt
#url = 'https://github.com/napo/geospatial_course_unitn/raw/master/data/istat/istat_administrative_units_generalized_2022.gpkg'
#urllib.request.urlretrieve(url ,"istat_administrative_units_generalized_2022.gpkg")
import warnings
warnings.filterwarnings('ignore')

TITLE = "Italy Housing prezzos"
SUB_TITLE = "Explore the Housing prezzos in Italy"

def normalize(col, range):
    newcol = ((col - col.min() ) / (col.max() - col.min() ) * range)
    return newcol

df = pd.read_parquet("italy_housing_price_rent_raw.parquet.gzip")

df['regione'] = df['regione'].str.lower()
df.regione = df.regione.replace({
    "friuli-venezia giulia": "friuli venezia giulia",
    "trentino-alto adige/s�dtirol": "trentino-alto adige",
    "trentino-alto-adige": "trentino-alto adige",
    "valle d'aosta/vall�e d'aoste": "valle d'aosta",

})

df['prezzo'] = df['prezzo'].str.replace('€', '')
df['prezzo'] = df['prezzo'].str.replace('.', '', regex=False)
df['prezzo'] = df['prezzo'].apply(lambda x: pd.to_numeric(x, errors='coerce') )
price_pre_region = df.groupby('regione').mean('prezzo').sort_values('prezzo', ascending=False)
price_pre_region = price_pre_region.reset_index()
price_pre_region['prezzo'] = price_pre_region['prezzo'].astype(float)
price_pre_region['prezzo'] = normalize(price_pre_region['prezzo'], 1)

#%%

map = folium.Map(
    location = [41.87194, 12.56738],
    zoom_start = 5.6,
    scrollWheelZoom = False,
    tiles = 'cartodbpositron'
)
#%%
choropleth = folium.Choropleth(
    geo_data='data/georef-italy-regione-millesime.geojson',
    data = price_pre_region,
    columns = ('regione', 'prezzo'),
    key_on='feature.properties.reg_name_lower',
    line_opacity=0.5,
    fill_opacity=0.2,
    highlight=True
)

#%%
choropleth.geojson.add_to(map)
st.write(price_pre_region)
st_map = st_folium(map, width=500, height=700)


#%%
