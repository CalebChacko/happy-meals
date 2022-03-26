# 😄 Happy Meals 🍴
This project is focused on utilizing Sentiment Analysis through natural language processing (NLP) to determine the highest rated recipes. 

## Overview
I love trying new recipes, expanding my horizon of tastes. However, sifting through recipes online can be difficult for a few reasons.

1. There are many ads crowding the screen
2. The ingredients to make the recipe are positioned at the bottom of the page
3. Many recipes have reviewers who rate the recipe high, but contradict themself with only placing negative comments *(Comments usually hold more weight than the rating number)*

Combining my interest for exploring new foods and a desire to learn more about machine learning models, I decided to create Happy Meals.

*The goal of this project is to design a streamlined process to make finding highly rated recipes more accessible.* 

This project uses a mixture of webscraping and sentiment analysis through Natural Language Processing (NLP). At a high level, the Webdriver will extract details and comments of multiple recipes from [Food Network](https://www.foodnetwork.com/), given an input search keyword. After extracting the data, the NLP model will assess each comment and rate it between 1 and 5 stars based on text such as: 'Good', 'Great', or 'Amazing'. The average rating of all comments in a recipe is taken and the top average rating of all recipes will be selected. 

## 🛠 Installation
**Pre-Requisite: Ensure you have Python 3.9 installed**

First, clone the repo, unzip the folder and open your favorite command terminal. Run the following commands:

`python -m pip install virtualenv` : When using Python, it's best to create separate python environments for each project. This allows for easier package dependency.

`python -m venv ./` : This command creates a virtual environment for this project. Ensure this command is run from the root directory

`./Scripts/Activate` : Activates the virtual environment. If it successfully activates, you will see `(Happy Meals)` on the left of the directory in your terminal. On Mac, this command is equivalent to `source /env/bin/activate`

`pip install -r ./requirements.txt` : After activating the virtual env, the python packages can be installed for the project with this command.

`python ./Models/model_setup.py` : This command builds the model used for sentiment analysis. It will be stored on your local machine. 

These 5 commands should be sufficient to setup the project on a local computer.

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
<img align='right' src="./assets/single_thread_workflow.png" width="250">

The algorithm is split into two separate components:
1. Scraping recipe information
2. Rating recipes using NLP model



### Web Scrape Recipes
For this project, I utilized recipes from [Food Network](https://www.foodnetwork.com/). I use Selenium to navigate the website and BeautifulSoup to parse the html. After extracting the input search query from `./Data/input.txt`, a Chrome Webdriver is instantiated and enters Food Network with the search field included. 

The driver first iterates through the search pages storing the URLs of each recipe in a list. It continues until it reaches X amount of recipes. This value is currently hardcoded, but will be a variable in future updates. 

After collecting enough links, it iterates through each link to extract recipe details. Before parsing the html, the driver clicks the "More Comments" button on the recipe page a few times to expand our dataset of comments. The html is then parsed and placed in a temporary csv file. By the end of this component, a csv file full of X recipes is saved in `./Data/Temp_Storage/<item>_recipes.csv`

### Rating Recipes
The second component focuses on evaluating the comments of each recipe using Natural Language Processing (NLP). While I would like to design my NLP tool for this project, I began with using a pre-trained BERT model. In the setup script, this model is downloaded to the user's system. 

> **BERT** <img src="./assets/bert.png" width="15"/>
> 
> BERT stands for [**Bidirectional Encoder Representation from Transformers**](https://arxiv.org/pdf/1810.04805.pdf). This pre-trained model was 
designed by Google in 2018. At a high level, BERT can identify sentence context to predict the current word in the sentence. For example, given "The quick brown fox jumps over the lazy _____", BERT would take the context of the sentence to determine which word would best fit in the blank. This has many applications including finding the sentiment of a sentence. A comment such as "The smell of the broccoli was putrid!" would be assessed as a negative phrase and would rated a 1. If it received a comment such as "This broccoli was delicious. It taasted like a mouthful of heaven!", it would assess the phrase as positive and give it a 5 star rating.  

The algorithm iterates through each recipe. Each comment from the recipe is then given to the model. Once all comments are evaluated, the average of the recipe comments is calculated. This continues for all recipes. At the end, the file is sorted by *rating* and then by *time*. This filter may be adjustable in a future update. 

The top rated recipe is then placed in the output.txt with its details.

## Challenges
While building this project, I struggled with two issues. 

First, the project required webscraping data. I found Food Network's website difficult to scrape at times as some of the element were hard to locate. Using online tips for parsing html, I learned to incorporate better Selenium practices to create a streamlined webscraping script.

Second, I found it challenging to parse arrays within a DataFrame cell that was imported from a csv. This took some tinkering and research to find the solution. In the end, I added `literal_eval()` from the `ast` library for support. It helps anaylze the syntax of the data using an abstract syntax tree. 

The future challenges I can foresee are listed below in the next updates.

## ✨ Future Updates
I'm happy with the result of the project so far. It reliably outputs recipe ingredients based on the sentiment of recipe reviews. 

However, this project is not user-friendly. At this time, it requires programming experience to setup and run the program. This is acceptable as I wanted to ensure it operated properly first before giving it a user-friendly design.
 
The next steps are to include:

**Automated Installation Script**

Users can simply run an executable to setup the environment and model.

**User Interface for Inputs and Outputs**

Rather than opening text files, the project will open a simple GUI. Users will be able to update the input and view the output. Additional inputs will be added including number of recipes to scan and what property to sort by (i.e *Time* rather than *Rating*)

**Parallelism Optimization**

The program runs too slow for a user to access in a reasonable time. To streamline this process, the program can be restructured with multiple threads.

<img src="./assets/parallel_workflow.png" width="400"/>

As shown in the diagram above, the program still instantiates a single Webdriver. Rather than opening a recipe, extracting the html, then moving onto the next recipe, the program will open all the recipes and store the html for each recipe. Once all recipe HTML are stored, multiple threads will extract and rate the comments at the same time. This should reduce the runtime of the program significantly


**Custom NLP Model**

BERT is an extraordinary pre-trained model. However, I would like to practice training a model on unstructured data, as most of my experience has focused on structured data.
