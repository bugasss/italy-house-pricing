import pandas as pd
import numpy as np
from deep_translator import GoogleTranslator
import re
from termcolor import colored
import warnings

warnings.filterwarnings('ignore')

print(colored("Cleaning data...", "blue", attrs=["bold"]))



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
        self.df['prezzo'] = self.df['prezzo'].str.replace('.', '', regex=False)
        self.df['prezzo'] = self.df['prezzo'].apply(lambda x: pd.to_numeric(x, errors='coerce') )

        self.df['bagni'] = self.df['bagni'].apply(lambda x: pd.to_numeric(x, errors='coerce') )

        self.df['stanze'] = self.df['stanze'].apply(lambda x: x[0] if x else x)

        self.df['m2'] = self.df['m2'].str.replace(r'\D', '')
        self.df['m2'] = self.df['m2'].str.replace('[^0-9\.]', '', regex=True)

        self.df['accesso disabili'] = self.df['piano'].str.find('disabili') > 0
        self.df['ascensore'] = self.df['piano'].str.find('ascensore') > 0

        self.df['piano'] = self.df['piano'].str.replace('Piano terra', '0')
        self.df['piano'] = self.df['piano'].str.replace('€', np.nan)

        self.df['piano'] = self.df['piano'].apply(lambda x: x[0] if x else x)

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

        self.df['spese condominio'] = self.df['spese condominio'].str.replace('/mese', '')

        self.df['spese condominio'] = self.df['spese condominio'].str.replace('€', '')

        return self.df


#%%
#clean_data = CleanHousingData('italy_housing_price_rent_raw.parquet.gzip')
#df = clean_data.clean_data()


#%%
