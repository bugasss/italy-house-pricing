import immobiliare_scraping as scraping
import clean_data as clean
import time
from termcolor import colored
import warnings
warnings.filterwarnings("ignore")

start = time.time()

try:
    scraping.main()
except:
    "No new data to scrape. Try tomorrow"

print(colored('All libraries imported', 'blue', attrs=['bold']))

clean.main()
print(colored("Done!", "blue", attrs=["bold"]))

end = time.time()
tot_time = round((end - start)/60, 2)
print(tot_time, "minutes")


#%%
