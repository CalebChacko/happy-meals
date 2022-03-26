import os
import pandas as pd
from Scrape import scrape_tools as st
from Scrape import foodnetwork as fn
from Rate import rate_recipes as rr
from ast import literal_eval

# SETUP
with open('./Data/input.txt') as f:
    lines = f.readlines()

user_search = lines[0]
user_search = user_search.replace(' ', '-')

view_browser = False
download_path = os.getcwd() + './Data/'

browser = st.setup_browser(view_browser, download_path)

# EXTRACT RECIPES
fn.search_recipes(browser, user_search, 3)
browser.close()

# RATE RECIPES
recipes = pd.read_csv('./Data/Temp_Storage/' + user_search + '_recipes.csv')
recipe = rr.rate_comments(recipes, user_search)

# OUTPUT INGREDIENTS
with open('./Data/Output/output.txt', 'w') as f:
    f.write('Name: ' + recipe['Name'] + '\n')
    f.write('Rating: ' + str(recipe['Rating']) + '\n')
    f.write('Time: ' + str(recipe['Time']) + ' minutes\n')
    f.write('Details: ' + str(recipe['Link']) + '\n')
    f.write('\n')
    f.write('Ingredients \n')
    ingrs = literal_eval(recipe[2])
    
    for line in ingrs:
        f.write(line)
        f.write('\n')
