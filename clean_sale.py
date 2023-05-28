import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
import re
from termcolor import colored
import warnings

warnings.filterwarnings('ignore')

print(colored("Cleaning data...", "blue", attrs=["bold"]))

def Translate(x):
    try:
        return GoogleTranslator(source='auto', target='en').translate(x)
    except:
        return x

#%%
class CleanHousingData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def read_data(self):
        self.df = pd.read_parquet(self.filepath)

    def clean_data(self):
        if self.df is None:
            self.read_data()

        self.df['prezzo'] = self.df['prezzo'].str.replace('€', '')
        self.df['prezzo'] = self.df['prezzo'].str.replace(r'[^0-9]+', '')

        self.df['bagni'] = self.df['bagni'].apply(lambda x: pd.to_numeric(x, errors='coerce') )

        self.df['stanze'] = self.df['stanze'].apply(lambda x: x[0] if x else x)

        self.df['m2'] = self.df['m2'].str.replace(r'\D', '')
        self.df['m2'] = self.df['m2'].str.replace('[^0-9\.]', '', regex=True)
        self.df = self.df.loc[self.df['m2'] != '']

        self.df['accesso disabili'] = self.df['piano'].str.find('disabili') > 0
        self.df['ascensore'] = self.df['piano'].str.find('ascensore') > 0

        self.df['piano'] = self.df['piano'].str.replace('Piano terra', '0')
        self.df['piano'] = self.df['piano'].str.replace('€', "")

        date_regex = r'(\d{2}/\d{2}/\d{4})'
        self.df['Riferimento e Data annuncio'] = self.df['Riferimento e Data annuncio'].str.extract(date_regex)

        tipologie = self.df['tipologia'].str.split('|', 0)
        self.df['tipologia immobile'] = [x[0] for x in tipologie if x[0]]

        for i in tipologie:
            if len(i) > 1:
                self.df['tipologia proprieta'] = i[1]
            else:
                self.df['tipologia proprieta'] = None

        for i in tipologie:
            if len(i) > 2:
                self.df['classe immobile'] = i[2]
            else:
                self.df['classe immobile'] = None

        self.df['locali'] = self.df['locali'].apply(lambda x: x[0] if x else x)

        # self.df['other_characteristics'] = self.df['other_characteristics'].str.replace(' ', '_')

        self.df['Data di inizio lavori e di consegna prevista'] = self.df['Data di inizio lavori e di consegna prevista'].str.extract(date_regex)

        return self.df

    def lower_case(self):
        self.df.columns = self.df.columns.str.lower()
        return self.df

    def clean_dates(self):
        self.df['Riferimento e Data annuncio'] = pd.to_datetime(self.df['Riferimento e Data annuncio'], format='%d/%m/%Y')
        self.df = self.df.loc[self.df['Riferimento e Data annuncio'] > '2023-01-01']
        return self.df

    def drop_columns(self):
        columns = ['prezzo', 'stanze', 'm2', 'bagni', 'piano',
                   'Riferimento e Data annuncio', 'contratto', 'tipologia', 'superficie',
                   'locali', 'totale piani edificio',
                   'other_characteristics', 'citta', 'quartiere', 'via', 'altre caratteristiche',
                   'spese condominio', 'cauzione', 'anno di costruzione', 'stato',
                   'riscaldamento', 'Climatizzatore', 'Efficienza energetica', 'certificazione energetica',
                   'Emissioni di CO₂', 'regione', 'accesso disabili',
                   'ascensore', 'tipologia immobile']
        self.df = self.df[columns]
        return self.df

    def save_data(self, filepath):
        self.df.to_parquet(filepath, compression='gzip')

    def translate(self):
        columns_eng = [Translate(x) for x in self.df.columns]
        cols_to_translate = ['contratto', 'tipologia', 'totale piani edificio',
                             'other_characteristics', 'Tipologia immobile']
        self.df.columns = columns_eng
        return self.df

    def main(self):
        self.read_data()
        self.clean_data()
        self.clean_dates()
        self.lower_case()
        #self.dropColumns()
        #self.translate()
        self.save_data("italy_housing_price_sale_clean.parquet.gzip")
        return self.df


#%%

#%%
df = pd.read_parquet("italy_housing_price_sale_raw.parquet.gzip")

#%%
df.columns
#%%
cleaner = CleanHousingData("italy_housing_price_sale_raw.parquet.gzip")
df = cleaner.main()
#%%
