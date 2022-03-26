import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def parse_time(cook_time):
    minutes = 0
    
    if 'hr' in cook_time:
        time_split = cook_time.split('hr')
        hour = int(time_split[0])
        minutes += int(time_split[0])*60
        cook_time = time_split[1]
        
    if 'min' in cook_time:
        time_split = cook_time.split('min')
        minutes += int(time_split[0])        
    return minutes

def extract_recipe(browser, url, first_time):
    browser.get(url)
    print(url)
    time.sleep(1)

    if first_time:
        # Pop up based on location
        browser.find_element(By.CLASS_NAME, "o-InternationalDialog__a-Button--Text").click()

    try:
        # Confirm this page is a recipe
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "comments-sort-toggle")))
    except:
        print('Error parsing: ', url)
        return []

    browser.find_element(By.CLASS_NAME, "comments-sort-toggle").click()
    # first_review = browser.find_element(By.XPATH, "//*[text()='Be the first to review']")
    if 'Be the first to review' not in browser.page_source:
        sort_by = browser.find_element(By.XPATH, "//*[@id='mod-user/comments-feed-1']/div[2]/div/ul/li[3]")
        sort_by.click()

        for i in range(5):
            try:
                browser.find_element(By.CLASS_NAME, "comments-more").click()
                time.sleep(0.2)
            except:
                break
    
    recipe_html = browser.page_source
    r_soup = BeautifulSoup(recipe_html, 'html.parser')

    name = r_soup.find('span', attrs={"class": "o-AssetTitle__a-HeadlineText"})
    cook_time = r_soup.find('span', attrs={"class": "o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total"})

    items = []
    i = 0
    for ingr in r_soup.find_all('span', attrs={"class": "o-Ingredients__a-Ingredient--CheckboxLabel"}):
        if i == 0:
            i += 1
            continue
        items.append(str(ingr.get_text()).strip())
        i += 1

    comments = []
    for c in r_soup.find_all('div', {"data-level": "0"}):
        c_soup = BeautifulSoup(str(c.contents), 'html.parser')
        comment = c_soup.find('div', attrs={"class": "comment-body"})
        if comment is None or len(comment) == 0:
            continue
        comments.append(str(comment.get_text()).strip())

    c_time = ""
    if cook_time is not None:
        c_time = parse_time(cook_time.get_text())

    r_name = url
    if name is not None:
        r_name = name.get_text()


    return [r_name, c_time, items, comments, url]


def search_recipes(browser, item, total_links):
    links = []
    num_links = 0
    i = 1

    while num_links < total_links:
        url = 'https://www.foodnetwork.com/search/' + item + '-/p/' + str(i+1)
    
        # collect all recipes from page
        search_page = requests.get(url).text
        soup = BeautifulSoup(search_page, 'html.parser')

        for tag in soup.find_all('section', attrs={"class": "o-RecipeResult"}):
            section_soup = BeautifulSoup(str(tag.contents))
            hrefs = section_soup.find_all('a')
            links.append('http:' + hrefs[0].get('href'))
            num_links += 1

        i += 1
            
    print('Num Recipes: ', len(links), ' Should be: ', total_links)

    cols = ['Name', 'Time', 'Ingredients', 'Comments', 'Link']
    df = pd.DataFrame([['ABC', '10 minutes', ['Nothing', 'Nothing'], ['check', 'check', 'check'], 'www.blah.com']], columns=cols)

    i = 0
    first = True
    for link in links:
        # if i > 1:
        #     break
        
        result = extract_recipe(browser, link, first)
        if len(result) == 0:
            continue

        recipe = pd.DataFrame([result], columns=cols)
        df = pd.concat([df, recipe], axis=0)
        df.to_csv('./Data/Temp_Storage/' + item + '_recipes.csv', index = False, header=True)
        i += 1
        
        if first:
            df = df.tail(df.shape[0] -1)
            first = False

    df.to_csv('./Data/Temp_Storage/' + item + '_recipes.csv', index = False, header=True)

    

