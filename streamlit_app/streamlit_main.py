import pandas as pd
import numpy as np
from datetime import date
import streamlit as st
import base64
import os

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
                   page_title="ITALY HOUSE PRICES",
                   page_icon=":🏠:")

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


#@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:icons/{img_format};base64,{bin_str}" width="40" height="40" />
        </a>'''
    return html_code


#%% FUNCTIONS

st.markdown("<h1 style='text-align: center; color: black;'>ITALIAN RENTS APP</h1>", unsafe_allow_html=True)

show_description = st.checkbox("SHOW DESCRIPTION", value="Yes", key="show_description")

if show_description:
    git_path = "https://github.com/tommella90"
    link_path = "https://www.linkedin.com/in/tommaso-ramella"
    git = get_img_with_href('icons/git.png', 'https://github.com/tommella90')
    lnkd = get_img_with_href('icons/linkedin.png', 'https://www.linkedin.com/in/tommaso-ramella')

    col1, col2, col3 = st.columns([1, 1, 2])

    st.write("-"*10)
    st.markdown("#### 🏠 THIS APP SHOWS THE AVERAGE RENT PRICES IN ITALY AND OTHER COOL STAFFS")
    with col1:
        st.write("my github:")
        st.markdown(git, unsafe_allow_html=True)
    with col2:
        st.write("my linkedin:")
        st.markdown(lnkd, unsafe_allow_html=True)
    with col3:
        st.write("Data source: [immobiliare.it](https://www.immobiliare.it/)")

    st.markdown("#### This app has 4 main functionalities:")
    st.markdown(""" 
    1) 🍕 **ITALIAN MAP**: shows the average price per municipality on the Italian map
    2) 📪 **MUNICIPALITY MAP**: select a municipality, and see the average price per neighbourhoods
    3) ⌚ **TIME SERIES ANALYSIS**: show the average price in Italy, per region, city and neighbourhoods
    4) 💰 **AFFORDABILITY**: choose a price range and compare what you can afford in different cities (squared meters, rooms, etc...)
    """)
    st.markdown("##### 📊 I upload new data every week, so stay tuned!")
    st.write("-"*10)

st.write("\n")
st.markdown("##### WHAT ARE YOU INTERESTED IN?")
option = st.selectbox(
    'choose an option',
    ('Italian Map', 'Neighbourhoods Map', 'Time-series', 'Affordability'),
    index=0, key="option", help="choose an option"
)


#%% MAPS
if option == "Italian Map":
    st.markdown("### **ITALIAN MAP** - MAP AVERAGE RENTS PRICES IN ITALY")
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
    st.markdown("### **NEIGHBOURHOODS MAP** - MAP AVERAGE RENTS PRICES PER CITY")
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
    st.markdown("### **TIME-SERIES** - DISPLAY AVERAGE RENTS PRICES IN ITALY, PER REGION, CITY AND NEIGHBOURHOODS OVER TIME")
    st.write(" - Select a time range (daily, weekly or monthly")
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
        return pd.read_parquet("dataframes/italy_housing_price_rent_clean.parquet.gzip")

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
