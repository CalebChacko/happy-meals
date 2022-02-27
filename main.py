import os
from Scraping import scrape_tools as st
from Scraping import foodnetwork as fn

user_search = 'spaghetti'

view_browser = False
download_path = os.getcwd() + './Storage/'
# browser = ''

browser = st.setup_browser(view_browser, download_path)

fn.search_recipes(browser, user_search)
