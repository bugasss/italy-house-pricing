import pandas as pd
import numpy as np
from datetime import date
import streamlit as st
import plotly.express as px

from maps_italy import MapPriceItaly
from map_neighbourhoods import MapPriceNeighbourhoods
from time_series_analysis import PriceTimeSeries
from affordability import Affordability

from pathlib import Path
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "main.css"

## CONFIG ##
st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded",
                   page_title="spotify_recommender",
                   page_icon=":🧊:")

m = st.markdown("""
<style>
section[data-testid="stSidebar"] .css-ng1t4o {{width: 10rem;}}

div.stButton > button:first-child {
    background-color: #141c7a;
    color: white;
    height: 3em;
    width: 5em;
    border-radius:10px;
    border:3px solid #000000;
    font-size:30px;
    font-weight: bold;
    margin: auto;
    display: block;
}


div.stButton > button:hover {
	background:linear-gradient(to bottom, #ce1126 5%, #ff5a5a 100%);
	background-color:#ce1126;
}

div.stButton > button:active {
	position:relative;
	top:3px;
	
}

</style>""", unsafe_allow_html=True)

import streamlit as st

TODAY = np.datetime64(date.today())

FULL_CALENDAR = pd.DataFrame(pd.date_range(start="2023-01-01", end=TODAY), columns=['datetime'])

REGIONI = ['Italy',
           'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
           'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche',
           'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana',
           'Veneto', 'Valle-D-Aosta', 'Trentino-Alto-Adige'
           ]



#%% FUNCTIONS

st.markdown("<h1 style='text-align: center; color: green;'>ITALIAN RENTS APP</h1>", unsafe_allow_html=True)

st.markdown("### This app show the average price of rents in Italy and other cool staffs")
st.markdown("##### **Data source:** [immobiliare.it](https://www.immobiliare.it/)")

st.write("-"*10)
option = st.selectbox(
    'WHAT ARE YOU INTERESTED TO?',
    ('Italian Map', 'Neighbourhoods Map', 'Time-series', 'Affordability')
)


#%% MAPS
if option == "Italian Map":
    st.markdown("### **ITALIAN MAP**")
    st.markdown("##### DISPLAY AVERAGE RENTS PRICES IN ITALY ON THE MAP")
    st.write("- Select a time and a price range of preference from the sidebar")

    italy_mapper = MapPriceItaly()
    time_start, time_end = italy_mapper.side_bar_time_range()
    min_price, max_price = italy_mapper.side_bar_price_range()

    italy_mapper.main(
        operation=italy_mapper.box_choice_math_operation(),
        date_start=time_start,
        date_end=time_end,
        min_price=min_price,
        max_price=max_price,
    )


elif option == 'Neighbourhoods Map':
    st.markdown("### **NEIGHBOURHOODS MAP**")
    st.markdown("##### DISPLAY AVERAGE RENTS PRICES PER CITY ON THE MAP")
    st.write("- Select a city from the sidebar to display the neighbourhoods prices")
    st.write("- Select a time and a price range of preference from the sidebar")
    neighbourhood_mapper = MapPriceNeighbourhoods()
    time_start, time_end = neighbourhood_mapper.side_bar_time_range()
    min_price, max_price = neighbourhood_mapper.side_bar_price_range()
    province = neighbourhood_mapper.side_bar_city()

    neighbourhood_mapper.main(
        date_start=time_start,
        date_end=time_end,
        min_price=min_price,
        max_price=max_price,
        operation=neighbourhood_mapper.box_choice_math_operation(),
        city=province
    )

elif option == "Time-series":
    st.markdown("### **TIME-SERIES**")
    st.markdown("##### DISPLAY AVERAGE RENTS PRICES IN ITALY, PER REGION, CITY AND NEIGHBOURHOODS OVER TIME")
    st.write(" - Select a region/city from the sidebar to display the neighbourhoods prices")
    st.write(" - Select a time and a price range of preference from the sidebar")

    time_serier_plotter = PriceTimeSeries()
    time_start, time_end = time_serier_plotter.sidebar_select_time_range()
    period = time_serier_plotter.sidebar_select_seasonality()
    max_price = time_serier_plotter.slider_price_limit()
    regions = time_serier_plotter.sidebar_select_regions()
    municipalities = time_serier_plotter.sidebar_select_municipalities()
    city = time_serier_plotter.sidebar_select_city()
    neighbourhoods = time_serier_plotter.sidebar_select_neighbourhoods(city)

    time_serier_plotter.main(period=period,
                             regions=regions,
                             municipalities=municipalities,
                             city=city,
                             neighbourhoods=neighbourhoods,
                             time_start=time_start,
                             time_end=time_end,
                             max_price=5000)



elif option == "Affordability":
    st.markdown("# **AFFORDABILITY**")

    @st.cache_data
    def load_data():
        return pd.read_parquet("../dataframes/italy_housing_price_rent_clean.parquet.gzip")

    df = load_data()
    st.markdown("#### CHOOSE A PRICE RANGE AND COMPARE WHAT YOU CAN AFFORD IN DIFFERENT CITIES")

    affordability = Affordability()
    time_start, time_end = affordability.sidebar_select_time_range()
    min_price, max_price = affordability.slider_price_limit()
    column = affordability.sidebar_select_column()
    types = affordability.sidebar_multiselect_type()

    st.markdown(f"### Your price range: {min_price}€ - {max_price}€")

    df = affordability.main(df, selected_types=types, column_name=column,
                            time_start=time_start, time_end=time_end,
                            min_price=min_price, max_price=max_price
                            )

#%%
