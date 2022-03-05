import os
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re

def extract_recipe(browser, url, first_time):
    url = 'http:' + url
    browser.get(url)
    time.sleep(1)

    if first_time:
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
    r_soup = BeautifulSoup(recipe_html, 'html.parser')

    try:
        name = r_soup.find('span', attrs={"class": "o-AssetTitle__a-HeadlineText"})
        r_time = r_soup.find('span', attrs={"class": "o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total"})
        ingredients = r_soup.find('div', attrs={"class": "o-Ingredients__m-Body"})
        comments = r_soup.find('div', attrs={"class": "comments loaded"})

        print('Name:', name)
        print('Time:', r_time)
        print('Ingredients:', str(ingredients.contents)[0:100])
        print('Comments:', str(comments.contents)[0:100])
    except:
        with open(os.getcwd() + '/error_html.txt', 'w') as f:
            f.write(str(recipe_html))
            f.close()

    return [name, r_time, ingredients, comments]


def search_recipes(browser, item, num_pages):

    links = []
    num_links = 0
    total_links = 25
    i = 1

    while num_links < total_links:
        url = 'https://www.foodnetwork.com/search/' + item + '-/p/' + str(i+1)
    
        # collect all recipes from page
        search_page = requests.get(url).text
        soup = BeautifulSoup(search_page, 'html.parser')

        for tag in soup.find_all('section', attrs={"class": "o-RecipeResult"}):
            section_soup = BeautifulSoup(str(tag.contents))
            hrefs = section_soup.find_all('a')
            links.append(hrefs[0].get('href'))
            num_links += 1

        i += 1
            
    print('Num Recipes: ', len(links), ' Should be: ', total_links)

    data = []

    i = 0
    first = True
    for link in links:
        if i > 1:
            break
        elif i > 0:
            first = False

        result = extract_recipe(browser, link, first)
        data.append(result)
        
        i += 1

    

