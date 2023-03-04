from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib import *
import requests
import time
import random
from termcolor import colored
import warnings
import clean_data as clean

import re

columns = ['price_bis', 'rooms', 'm2', 'bathrooms', 'floor', 'description',
              'condominium_expenses', 'energy_class', 'date',
              'contract', 'typology', 'surface', 'rooms2', 'floor2',
              'total_floors', 'availability', 'other_features',
              'price', 'condominium_expenses2', 'year_of_build', 'condition',
              'heating', 'air_conditioning', 'energy_efficiency', 'city',
              'neighborhood', 'address', 'href', 'car_parking',
              'renewable_energy_performance_index',
              'energy_performance_building', 'housing units',
              'start_end_works', 'current_building_use','energy_certification', 'co2_emissions',
              'deposit', 'type of sale', 'date_sell', 'minimum offer', 'minimum rise',
              'expense book debt', 'unpaid contribution',
              'number of buildings', 'updated on', 'cadastral data',
              'court', 'additional fees', 'procedure number']


warnings.filterwarnings("ignore")


tipologie = ['vendita', 'affitto']
regioni = ['lombardia', 'piemonte', 'veneto', 'emilia-romagna', 'toscana', 'lazio', 'campania',
           'sicilia', 'sardegna', 'puglia', 'abruzzo', 'marche', 'liguria',
           'friuli-venezia-giulia', 'trentino-alto-adige', 'umbria', 'molise',
           'basilicata', 'valle-d-aosta']


def read_parquet():
    try:
        return pd.read_parquet('italy_housing_price_raw.parquet.gzip')
    except:
        df = pd.DataFrame()
        return df


def get_downloaded_hrefs(df):
    hrefs = df['href'].tolist()
    return hrefs


def get_all_webpages(limit, regione):
    urls = []
    for tipologia in tipologie:
        urls.append(f"https://www.immobiliare.it/{tipologia}-case/{regione}/?criterio=rilevanza")
        for page in range(2, limit):
            url = f"https://www.immobiliare.it/{tipologia}-case/{regione}/?criterio=rilevanza&pag={page}"
            urls.append(url)
        return urls

"""
def get_all_webpages(limit):
    urls = []
    for tipologia in tipologie:
        for regione in regioni:
            urls.append(f"https://www.immobiliare.it/{tipologia}-case/{regione}/?criterio=rilevanza")
            for page in range(2, limit):
                url = f"https://www.immobiliare.it/{tipologia}-case/{regione}/?criterio=rilevanza&pag={page}"
                urls.append(url)
    return urls
"""

def get_all_announcements_urls(all_pages, downloaded):
    all_announcements_urls = []

    for index, url in enumerate(all_pages):
        try:
            if index % 10 == 0:
                print("Page: ", index, " of ", len(all_pages))
            response = requests.get(url)
            soup = bs(response.content, "html.parser")
            page_urls = soup.select(".in-card__title")
            page_urls = [url.get("href") for url in page_urls]
            page_urls_new = [url for url in page_urls if url not in downloaded]
            all_announcements_urls.append(page_urls_new)
            all_announcements_flat = [item for sublist in all_announcements_urls for item in sublist]
        except:
            print(colored('ERROR in', 'red'))
            print(colored(url, 'red'))
            pass

    return all_announcements_flat

# GO TO EACH ANNOUNCEMENT AND GET INFO
def get_home_soup(url):
    response = requests.get(url)
    soup = bs(response.content)
    return soup, url


# GET PRICE
def get_price(soup):
    div2 = soup.select(".nd-list__item.in-feat__item.in-feat__item--main")
    return div2[0].get_text()


# GET INFORMATION ABOUT THE
def get_main_items(soup):
    main_items = soup.select(".nd-list__item.in-feat__item")
    items_label = ["price", "rooms", "m2", "bathrooms", "floor"]
    items_value = [item.get_text() for item in main_items]
    d_items_main = dict(zip(items_label, items_value))
    return d_items_main


# OTHER ITEMS
def get_other_items(soup):
    other_items = soup.select(".in-realEstateFeatures__list")
    items_label = ["description", "spese_condominio", "energy_class"]
    items_value = [item.get_text() for item in other_items]
    d_items_others = dict(zip(items_label, items_value))
    return d_items_others


# GET ALL ITEMS
def get_all_items(soup):
    all_items = soup.select(".in-realEstateFeatures__title")
    all_items_labels = [item.get_text() for item in all_items]
    all_values = soup.select(".in-realEstateFeatures__value")
    all_items_values = [item.get_text() for item in all_values]
    d_all = dict(zip(all_items_labels, all_items_values))
    return d_all


# ADDRESS
def get_address(soup):
    address = soup.select(".in-location")
    address = [a.get_text() for a in address]
    location_id = ["city", "neighborhood", "address"]
    d_location = dict(zip(location_id, address))
    return d_location


# CREATE PANDAS DATAFRAME
def make_dataframe(href):
    soup, url = get_home_soup(href)
    mergedDict = get_main_items(soup) | get_other_items(soup) | get_all_items(soup) | get_address(soup)
    df = pd.DataFrame(columns=columns)
    df = df.append(mergedDict, ignore_index=True)
    df = pd.DataFrame(mergedDict, index=[0])
    df['href'] = url
    return df


def find_new_announcements(df, all_announcements_urls):
    href_done = df['href'].tolist()
    diff = list(set(all_announcements_urls).difference(set(href_done)))
    return diff


def main(limit, regione):
    sleep = random.randint(1, 10)/10

    print(colored(f"Fetching the urls...", 'blue', attrs=['bold']))
    df = read_parquet()
    downloaded_hrefs = get_downloaded_hrefs(df)
    all_pages = get_all_webpages(limit, regione)
    urls_to_scrape = get_all_announcements_urls(all_pages, downloaded_hrefs)
    new_urls = find_new_announcements(df, urls_to_scrape)

    if len(new_urls)==0:
        print(colored('No new data to scrape. Try tomorrow', 'yellow'))
        pass

    else:
        print(colored(f"Found {len(new_urls)} new announcements to scrape", 'green'))
        print(colored(f"Creating the new data...", 'blue', attrs=['bold']))

        df_update = pd.DataFrame(columns = columns)
        for index, url in enumerate(new_urls):
            if index % 100 == 0:
                print(index, "/", len(new_urls))
            ads_info = make_dataframe(url)
            df_new = pd.concat([df_update, ads_info], axis=0)
            time.sleep(sleep)

        df_new = clean.main(df)

        df_updated = pd.concat([df, df_update], axis=0)

        df_updated.to_parquet('italy_housing_price_raw.parquet.gzip', compression='gzip')
        print(colored(f"Saved {len(new_urls)} more annoucements", 'green', attrs=['bold']))




#%%
main(6, 'piemonte')

#%%

df = read_parquet()
downloaded_hrefs = get_downloaded_hrefs(df)
all_pages = get_all_webpages(4, "calabria")
urls_to_scrape = get_all_announcements_urls(all_pages, downloaded_hrefs)
new_urls = find_new_announcements(df, urls_to_scrape)

if len(new_urls)==0:
    print(colored('No new data to scrape. Try tomorrow', 'yellow'))
    pass


df_update = pd.DataFrame()
for index, url in enumerate(new_urls):
    if index % 100 == 0:
        print(index, "/", len(new_urls))
    ads_info = make_dataframe(url)
    df_new = pd.concat([df_update, ads_info], axis=0)

#%%
df_new.columns


#%%
df_new = clean.main(df)

#%%
df_updated = pd.concat([df, df_update], axis=0)

df_updated.to_parquet('italy_housing_price_raw.parquet.gzip', compression='gzip')
print(colored(f"Saved {len(new_urls)} more annoucements", 'green', attrs=['bold']))



#%%

#%%
df = pd.DataFrame(columns=columns)
df2 = pd.merge(df, df_new, how='inner')
#%%
