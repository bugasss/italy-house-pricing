import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer


#%%
df = pd.read_parquet('italy_housing_price_rent_clean.parquet.gzip')

#%%
df.isna().sum()

#%%
df = df[['prezzo', 'm2', 'stanze', 'bagni', 'piano', 'riferimento e data annuncio', 'contratto',
         'tipologia', 'locali', 'posti auto', 'citta', 'regione', 'quartiere', 'stato',
         'riscaldamento', 'efficienza energetica', 'accesso disabili', 'ascensore', 'tipologia immobile']]
df.dtypes

#%%
df.columns

#%% input missing values
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
imp_mean.fit(df)
df = imp_mean.transform(df)

#%%
df['m2'] = df['m2'].astype('float64')


#%%
df['m2'].str.replace('', np.nan)
#%%
df.loc[df['m2'] == '']
#%%
