from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from ast import literal_eval


def get_rating(tokenizer, model, comment):
    tokens = tokenizer.encode(comment, return_tensors='pt')
    result = model(tokens)
    rating = int(torch.argmax(result.logits)) + 1
    return rating


def rate_comments(recipes, search):
    recipes['Comments'] = recipes['Comments'].apply(literal_eval)
    model = torch.load('./Models/bert_sentiment_model')
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    avg_rating = [0] * len(recipes.index)
    for i in range(len(recipes.index)):
        print(i)
        comments = recipes['Comments'].iloc[i]
        ratings = []
        for c in comments:
            # print(c)
            if c == '':
                continue
            elif len(c) > 512:
                # split into smaller parts
                # print(c)
                ratings.append(get_rating(tokenizer, model, c[:512]))
                
            else:
                ratings.append(get_rating(tokenizer, model, c))
            
        avg_rating[i] = (sum(ratings)/len(ratings)) if (len(ratings) > 0) else 0
        
    recipes['Rating'] = avg_rating
    recipes = recipes.sort_values(['Rating', 'Time'], ascending=[False, True]).reset_index(drop=True)
    # recipes.drop(index=recipes.index[0], axis=0, inplace=True)
    recipes.to_csv('./Data/Output/rated_' + search +'_recipes.csv', index = False, header=True)

    return recipes.iloc[0]