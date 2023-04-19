# MILANO HOUSE ANNOUNCEMENTS DATASET CREATION 
## WEB SCRAPING & BEAUTIFUL SOUP
 - The repository contains a dataframe with houses annoucements in Milan, web-scraped ah this [link](https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza) with Beautifull Soup

- If you run the scripts, they will automatically update the dataframe with all the new annoucements. 
Over time, it will be possibile to perform time-series analysis. 

  - [scraping_rents.py](https://github.com/tommella90/italy-house-pricing/blob/main/scraping_rents.py) and [scraping_sale.py](https://github.com/tommella90/italy-house-pricing/blob/main/scraping_sale.py) update the dataframe with all the non already existing announcements on the website. 
  - [clean_data.py](https://github.com/tommella90/milano-housing-price/blob/main/clean_data.py) cleans the data and returns a zipped csv with a pandas dataframe inside (only for rents). 
  - [main.py](https://github.com/tommella90/milano-housing-price/blob/main/clean_data.py) runs the scraping automatically. Can also be called with docker. 

____________________________________
***How to use***:
____________________________________
### 1 GIT REPOSITORY
In git run:
```
git clone https://github.com/tommella90/italy-housing-price/
```
In the new folder run:
```
pip install requirements.txt
```
To create the data, run:
```
python main.py
```

### 2 DOCKER IMAGE
Download this [docker image](https://hub.docker.com/repository/docker/tommella90/milano-housing/general) 


