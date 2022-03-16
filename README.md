# Recipe Recommendation using Sentiment Analysis
## Overview
I love trying new recipes, expanding my horizon of tastes. However, sifting through recipes online can be difficult for a few reasons.
1. There are many ads crowding the screen
2. The ingredients to make the recipe are positioned at the bottom of the page
3. Many recipes have reviewers who rate the recipe high, but only negative comments.

Combining my interest for new foods and a desire to learn more about machine learning models, I decided to create _____ .
This project uses a mixture of python, webscraping, and sentiment analysis through NLP. 

*The goal of this project is to design a streamlined process to make finding highly commented recipes more accessible.* 

## 🛠 Installation
**Pre-Requisite: Ensure you have Python 3.9 installed**

First, clone the repo. Unzip the folder and open your favorite command terminal. Run the following commands:

`python -m pip install virtualenv` : When using Python, it's best to create separate python environments for each project. This allows for easier package dependency.

`python -m venv ./` : This command creates a virtual environment for this project. Ensure this command is run from the root directory

`./Scripts/Activate` : Activates the virtual environment. If it successfuly activates, you will see `(sentiment-analysis-recipes)` on the left of the directory in your terminal. On Mac, this command is equivalent to `source /env/bin/activate`

`pip install -r ./requirements.txt` : After activating the virtual env, the python packages can be installed for the project with this command.

These 4 commands should be sufficient to setup the project on a local computer.

## 📝 Instructions
Running a recipe search is simple! 

First, modify `./Data/input.txt` with your desired dish and save the text file. 

As a demonstration, I'll use 🥦 Broccoli 🥦
```
Broccoli
```
 

Next, run `python main.py` from the terminal inside of the activated virtual environment. The explanation of the script structure is defined below. 

Afterwards, open `./Data/Output/output.txt`. Inside the file, there are details related to the top rated recipe based on our sentiment analysis!

```
Name: Broccoli and Green Beans
Rating: 4.56
Time: 35 minutes
Details: http://www.foodnetwork.com/recipes/giada-de-laurentiis/broccoli-and-green-beans-recipe2-1940842

Ingredients:
8 cups broccoli florets (about 1 1/2 pounds)
1/2 pound green beans
2 tablespoons cup extra-virgin olive oil
2 cloves garlic, sliced thin
1/2 teaspoon crushed red pepper flakes, plus more if desired
Sea salt and freshly ground black pepper
```

From my `broccoli` search, the program found a recipe called `Broccoli and Green Beans`. The *rating* represents the average sentiment rating of the comments found within the recipe. 4.56 stars is a great review! The *time* to complete the recipe is 36 minutes and the instructions can be found in further *detail* in the link. Finally, the *ingredients* for this recipe are listed at the bottom. 
 

## 💻 Algorithm Structure
The algorithm is split into two separate components:
1. Scraping recipe information
2. Rating recipes using NLP model

### Web Scrape Recipes
For this project, I utilized recipes from [Food Network](https://www.foodnetwork.com/). I use Selenium to navigate the website and BeautifulSoup to parse the html. After extracting the input search query from `./Data/input.txt`, a Chrome Webdriver is instantiated and enters Food Network with the search field included. 

The driver first iterates through the search pages storing the URLs of each recipe in a list. It continues until it reaches X amount of recipes. This value is currently hardcoded, but will be a variable in future updates. 

After collecting enough links, it iterates through each link to extract recipe details. Before parsing the html, the driver clicks the "More Comments" button on the recipe page a few times to expand our dataset of comments. The html is then parsed and placed in a temporary csv file. By the end of this component, a csv file full of X recipes is saved in `./Data/Temp_Storage/<item>_recipes.csv`

### Rating Recipes
The second component focuses on evaluating the comments of each recipe using Natural Language Processing (NLP). While I would like to design my NLP tool for this project, I began with using a pre-trained BERT model. In the setup script, this model is downloaded to the user's system. 

**BERT**

*Details about BERT*

The algorithm iterates through each recipe. Each comment from the recipe is then given to the model. Once all comments are evaluated, the average of the recipe comments is calculated. This continues for all recipes. At the end, the file is sorted by *rating* and then by *time*. This filter may be adjustable in a future update. 

The top rated recipe is then placed in the output.txt with its details.



## ✨ Future Updates
I'm happy with the result of the project so far. It reliably outputs recipe ingredients based on the sentiment of recipe reviews. 

However, this project is not user-friendly. At this time, it requires programming experience to setup and run the program. This is acceptable as I wanted to ensure it operated properly first before giving it a user-friendly design.
 
The next steps are to include:
* Automated Installation Script
* User Interface for Inputs and Outputs
* Algorithm Optimization
    * Concurrency Additions
* Custom NLP Model
