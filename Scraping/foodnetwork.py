
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re

def search_recipes(browser, item):
    url = 'https://www.foodnetwork.com/search/' + item + '-'
    
    # collect all recipes from page
    search_page = requests.get(url).text
    soup = BeautifulSoup(search_page, 'html.parser')
    css_selector = "#mod-site-search-results-1 > section:nth-child(2)" \
                    " > div > div > div.m-MediaBlock__m-TextWrap > h3 > a"
    h3 = soup.select(css_selector)
    # recipes = soup.find_all("a", attrs={'href': re.compile("^//www.foodnetwork.com/recipes/")})
    # #mod-site-search-results-1 > section:nth-child(2) > div > div > div.m-MediaBlock__m-TextWrap > h3 > a
    # print(recipes[0])
    print(len(h3))
    # print(h3)

    # browser.get(url)

    # go to first recipe
    test = "https://www.foodnetwork.com/recipes/tyler-florence/spaghetti-alla-carbonara-recipe-1914140"
    browser.get(test)
    browser.find_element(By.CLASS_NAME, "o-InternationalDialog__a-Button--Text").click()
    browser.find_element(By.CLASS_NAME, "comments-sort-toggle").click()
    browser.find_element(By.XPATH, "//*[@id='mod-user/comments-feed-1']/div[2]/div/ul/li[3]").click()
    for i in range(5):
        try:
            browser.find_element(By.CLASS_NAME, "comments-more").click()
            time.sleep(0.2)
        except:
            break
    
    recipe_html = browser.page_source
    print(recipe_html[0:100]) 
    r_soup = BeautifulSoup(recipe_html, 'html.parser')
    print(r_soup)
    ingredients = r_soup.find('o-Ingredients__m-Body')
    print(ingredients)

    data = []

