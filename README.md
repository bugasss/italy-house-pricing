# HOUSE PRICES IN ITALY
### This repository contains data on house rents and sales announcements in Italy, scraped with Beautifull Soup on [Immobiliare.com](https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza)

The main scripts download (**scraping_rents.py** and **scraping_sales.py** and clean the data (**clean_rents.py** and **clean_sales.py**)
The **main.py** runs the previous scripts, automatically scraping and cleaning the data. If you run it, you have to specify the option: *how many webpages do you want to scrapre?*. 

It also contains the **STREAMLIT APP**, with 4 main functionalities: 
1) ITALIAN MAP: shows the average price per municipality on the Italian map 
2) MUNICIPALITY MAP: select a municipality, and see the average price per neighbourhoods 
3) TIME SERIES ANALYSIS: show the average price in Italy, per region, city and neighbourhoods
4) AFFORDABILITY: choose a price range and compare what you can afford in different cities (squared meters, rooms, etc...)

[link](https://tommella90-italy-house-prici-streamlit-appstreamlit-main-p06j3n.streamlit.app/)
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


