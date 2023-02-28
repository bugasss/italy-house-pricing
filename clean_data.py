import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
import re
import warnings

warnings.filterwarnings('ignore')

def upload_data():
    df = pd.read_parquet('milano_housing_price_raw.parquet.gzip', engine='fastparquet')
    df.columns = ['price_bis', 'rooms', 'm2', 'bathrooms', 'floor', 'description',
                  'condominium_expenses', 'energy_class', 'date',
                  'contract', 'typology', 'surface', 'rooms2', 'floor2',
                  'total_floors', 'availability', 'other_features',
                  'price', 'condominium_expenses2', 'year_of_build', 'condition',
                  'heating', 'air_conditioning', 'energy_efficiency', 'city',
                  'neighborhood', 'address', 'href', 'car_parking',
                  'renewable_energy_performance_index',
                  'energy_performance_building', 'housing units',
                  'start_end_works', 'current_building_use',
                  'energy_certification', 'co2_emissions']
    return df


def Translate(italian_input):
    return GoogleTranslator(source='auto', target='en').translate(italian_input)


def clean_data(df):

    df['price'] = df['price'].str.replace('€', '')
    df['price'] = df['price'].str.replace('.', '', regex=False)
    df['price'] = df['price'].apply(lambda x: pd.to_numeric(x, errors='coerce') )

    df['m2'] = df['m2'].str.replace(r'\D', '')

    df['bathrooms'] = df['bathrooms'].apply(lambda x: np.nan if x and "€" in x else x)
    df['floor'] = df['floor'].apply(lambda x: np.nan if x and "€" in x else x)

    df['prezzo'], df['condominium_expenses'] = df['condominium_expenses'].str.split('condominio€ ', 1).str
    df['condominium_expenses'] = df['condominium_expenses'].str.replace('/mese', '')
    df.drop(columns=['prezzo'])

    date_regex = r'(\d{2}/\d{2}/\d{4})'
    df['date'] = df['date'].str.extract(date_regex)

    df['elevator'] = df['floor2'].apply(lambda x: 1 if x and "ascensore" in x else 0)
    df['floor_level'] = df['floor2'].apply(lambda x: x[0] if x else x)
    df['floor_level'] = df['floor_level'].str.replace('P', '0')

    df['contract'] = df['contract'].str.replace(',', ' |')
    df['contract'] = df['contract'].str.replace('-', ' - ')

    df['energy_efficiency'] = df['energy_efficiency'].str.replace('anno', 'year')

    df['total_floors'] = df['total_floors'].str.replace('piani', 'floors')
    df['total_floors'] = df['total_floors'].str.replace('piano', 'floor')

    df['other_features'].unique()

    df['heating_centralized'], df['heating_radiator'], df['heating_gas'] = df['heating'].str.split(',', 2).str

    df['air_conditiong_centralized'], df['air_conditioning_heat'] = df['air_conditioning'].str.split(',', 1).str

    df['renewable_energy_performance_index_KWh/m2'] = df['renewable_energy_performance_index'].str.replace(r'\D', '')

    df['air_conditioning_heat'].unique()

    df['air_conditioning_heat'] = df['air_conditioning_heat'].str.replace("freddo/caldo", "cold/hot")
    df['air_conditioning_heat'] = df['air_conditioning_heat'].str.replace("freddo", "cold")
    df['air_conditioning_heat'] = df['air_conditioning_heat'].str.replace("caldo", "hot")

    df['housing units'] = df['housing units'].str.replace(r'\D', '')

    df["air_conditioning_heat"].replace({np.nan: None}, inplace=True)
    df["heating_gas"].replace({np.nan: None}, inplace=True)
    df["heating_radiator"].replace({np.nan: None}, inplace=True)
    df['air_conditioning_heat'] = df['air_conditioning_heat'].str.lower()

    columns_to_drop = ['surface', 'renewable_energy_performance_index', 'prezzo',
                       'rooms2', 'description', 'address', 'price_bis', 'href',
                       'energy_class', 'condominium_expenses2', 'floor2', 'heating']

    df.drop(columns=columns_to_drop, inplace=True)
    return df

def translate_to_english(string):
    return GoogleTranslator(source='auto', target='en').translate(string)


def replace_with_english(df, col):
    list_tokens = df[col].unique()
    list_tokens = [x for x in list_tokens if x is not None]
    list_tokens_eng = [translate_to_english(x) for x in list_tokens if x]
    translation = dict(zip(list_tokens, list_tokens_eng))
    df[col].replace(translation, inplace=True)

def translate_dataframe_to_english(df, cols_to_translate):
    for col in cols_to_translate:
        replace_with_english(df, col)
    return df

def create_cleaned_data(df):
    df.to_csv('milano_housing_price_clean.csv', index=False)
    df.to_parquet('milano_housing_price_clean.parquet.gzip', engine='fastparquet')
    print('data cleaned and saved')
    return df

# main
cols_to_translate = ['contract', 'typology', 'availability', 'condition', 'availability',
                     'air_conditioning', 'energy_performance_building', 'heating_radiator',
                     'heating_gas', 'heating_centralized', 'air_conditiong_centralized']

categorical_columns = ['contract', 'typology', 'availability','other_features', 'condition',
                       'air_conditioning', 'energy_efficiency', 'city', 'neighborhood',
                       'housing units', 'current_building_use', 'heating_centralized',
                       'heating_radiator', 'heating_gas', 'air_conditiong_centralized',
                       'air_conditioning_heat']
def main():
    df = upload_data()
    df = clean_data(df)
    for col in categorical_columns:
        df[col] = df[col].str.lower()
    df = translate_dataframe_to_english(df, cols_to_translate)
    create_cleaned_data(df)
    return df

