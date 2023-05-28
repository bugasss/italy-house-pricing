import pandas as pd
import scraping_sale as sale
import scraping_rents as rent_scraper
import time
from termcolor import colored
import warnings
warnings.filterwarnings("ignore")

#%%
df = pd.read_parquet('dataframes/italy_housing_price_rent_raw.parquet.gzip')
starting_n = len(df)

print("Starting n: ", starting_n)

regioni = ['lombardia', 'piemonte', 'veneto', 'emilia-romagna', 'toscana', 'lazio', 'campania',
           'sicilia', 'sardegna', 'puglia', 'abruzzo', 'marche', 'liguria', 'calabria'
           'friuli-venezia-giulia', 'trentino-alto-adige', 'umbria', 'molise',
           'basilicata', 'valle-d-aosta']


n_pages = int(input("How many pages do you want to scrape? "))

start = time.time()

# FETCHING RENTS
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored("1. RENT", 'blue', attrs=['bold']))
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored(f"Fetching the urls...", 'blue', attrs=['bold']))


for index, regione in enumerate(regioni):
    try:
        df = pd.read_parquet('dataframes/italy_housing_price_rent_raw.parquet.gzip')
        print(colored(f"{regione.upper()}, {index+1}/19", "green"))
        new_data = rent_scraper.main(n_pages, regione)
        df_updated = pd.concat([df, new_data], axis=0)
        df_updated.to_parquet('dataframes/italy_housing_price_rent_raw.parquet.gzip')
    except:
        pass

df_new = pd.read_parquet("dataframes/italy_housing_price_rent_raw.parquet.gzip")
ending_n = len(df_new)
print(colored(f"TOTAL NEW ANNOUNCEMENTS: {ending_n-starting_n}/{ending_n}", 'blue', attrs=['bold']))

print("\n\n")
print('_'*20)


# CLEANING
import clean_rents as rent_cleaner

# clean rents
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored("CLEANING RENTS...", 'blue', attrs=['bold']))
print(colored("_"*20, 'blue', attrs=['bold']))
df = pd.read_parquet('dataframes/italy_housing_price_rent_raw.parquet.gzip')


cleaner = rent_cleaner.DataCleaner(df)
df_clean = cleaner.clean_data(df)
df_clean = df_clean.reset_index(drop=True)
df_clean.to_parquet('dataframes/italy_housing_price_rent_clean.parquet.gzip')

print('_'*20)
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored("RENTS CLEANED", 'blue', attrs=['bold']))


#%%

df = pd.read_parquet('dataframes/italy_housing_price_sale_raw.parquet.gzip')
starting_n = len(df)

print("Starting n: ", starting_n)

regioni = ['lombardia', 'piemonte', 'veneto', 'emilia-romagna', 'toscana', 'lazio', 'campania',
           'sicilia', 'sardegna', 'puglia', 'abruzzo', 'marche', 'liguria', 'calabria', 'friuli-venezia-giulia',
           'trentino-alto-adige', 'umbria', 'molise', 'basilicata', 'valle-d-aosta']

n_pages = int(input("How many pages do you want to scrape? "))

start = time.time()

# RENTS
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored("1. RENT", 'blue', attrs=['bold']))
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored(f"Fetching the urls...", 'blue', attrs=['bold']))


for index, regione in enumerate(regioni):
    try:
        df = pd.read_parquet('dataframes/italy_housing_price_sale_raw.parquet.gzip')
        print(colored(f"{regione.upper()}, {index+1}/19", "green"))
        new_data = rent_scraper.main(n_pages, regione)
        df_updated = pd.concat([df, new_data], axis=0)
        df_updated.to_parquet('dataframes/italy_housing_price_sale_raw.parquet.gzip')
    except:
        pass


df_new = pd.read_parquet("dataframes/italy_housing_price_sale_raw.parquet.gzip")
ending_n = len(df_new)
print(colored(f"TOTAL NEW ANNOUNCEMENTS: {ending_n-starting_n}/{ending_n}", 'blue', attrs=['bold']))

print("\n\n")
print('_'*20)

#%%
