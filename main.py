import scraping_sale as sale
import scraping_rents as rent
#import clean_data as clean
import time
from termcolor import colored
import warnings
warnings.filterwarnings("ignore")

regioni = ['lombardia', 'piemonte', 'veneto', 'emilia-romagna', 'toscana', 'lazio', 'campania',
           'sicilia', 'sardegna', 'puglia', 'abruzzo', 'marche', 'liguria',
           'friuli-venezia-giulia', 'trentino-alto-adige', 'umbria', 'molise',
           'basilicata', 'valle-d-aosta']

n_pages = 2

start = time.time()

# RENTS
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored("1. RENT", 'blue', attrs=['bold']))
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored(f"Fetching the urls...", 'blue', attrs=['bold']))

for index, regione in enumerate(regioni):
    try:
        print(colored(f"scraping: {regione}, {index+1}/19", "green"))
        rent.main(n_pages, regione)
    except:
        print("No new data to scrape. Try tomorrow")

print("\n\n")

# SALES
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored("2. SALE", 'blue', attrs=['bold']))
print(colored("_"*20, 'blue', attrs=['bold']))
print(colored(f"Fetching the urls...", 'blue', attrs=['bold']))

for index, regione in enumerate(regioni):
    try:
        print(colored(f"scraping: {regione}, {index+1}/19", "green"))
        sale.main(n_pages, regione)
    except:
        print("No new data to scrape. Try tomorrow")

print(colored('SCRAPING: DONE!', 'blue', attrs=['bold']))

end = time.time()
tot_time = round((end - start)/60, 2)
print(tot_time, "minutes")


#%%
