
# importing modules>>>>>>>>>>>>>>>>>>>>>>>
import math
import re

import test
import pyrebase
import requests
from fuzzywuzzy import fuzz

import cosine_similarity as keywordVal
import configurations



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# TODO😎️- estimate accuracy using confusion matrix  test (Machine Learning)


'''
excellent = 1
very good = 2
good = 3
average = 4
poor = 5
very poor = 6

Grammar:
y = 1
n = 0
'''


def givVal(model_answer, keywords, answer, out_of):
    # KEYWORDS =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # TODO : Enhacnce this thing
    if (len(answer.split())) <= 5:    # if the answer is too small neglect the answer 
        return 0
   
    k = keywordVal.givKeywordsValue(model_answer,answer)
    
    #TODO: add synonym checking done #DONE: added in cosine similarity part
    
    
    
    
    
    #TODO: addding extra keywords for model answers each time using data scraping
    
    
    
    
    
    

    




# GRAMMAR =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    req = requests.get("https://api.textgears.com/check.php?text=" + answer + "&key=JmcxHCCPZ7jfXLF6")
    no_of_errors = len(req.json()['errors'])

    if no_of_errors > 5  or k==6 :
        g = 0
    else:
        g = 1

 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   


# Fuzzyscore =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    q = math.ceil(fuzz.token_set_ratio(model_answer, answer) * 6 / 100)

    print("Keywords : ", k)
    print("Grammar  : ", g)
    print("Fuzzy score      : ", q)

    predicted = test.predict(k, g, q)
    
    result = predicted * out_of / 10
    return result[0]

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# DataBase related things =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

firebsevar = pyrebase.initialize_app(config=configurations.config)
db = firebsevar.database()
##print(db.child("model_answers").get().val())
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Getting Model answers =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
model_answer1 = db.child("model_answers").get().val()[1]['answer']
out_of1 = db.child("model_answers").get().val()[1]['out_of']


# add a methode for generation of keywords

keywords1 = db.child("model_answers").get().val()[1]['keywords']
keywords1 = re.findall(r"[a-zA-Z]+", keywords1)

model_answer2 = db.child("model_answers").get().val()[2]['answer']
out_of2 = db.child("model_answers").get().val()[2]['out_of']
keywords2 = db.child("model_answers").get().val()[2]['keywords']
keywords2 = re.findall(r"[a-zA-Z]+", keywords2)

model_answer3 = db.child("model_answers").get().val()[3]['answer']
out_of3 = db.child("model_answers").get().val()[3]['out_of']
keywords3 = db.child("model_answers").get().val()[3]['keywords']
keywords3 = re.findall(r"[a-zA-Z]+", keywords3)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



# print(model_answer1)
# print(model_answer2)
# print(model_answer3)

# print(keywords1)
# print(keywords2)
# print(keywords3)



#Getting other answers =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
all_answers = db.child("answers1").get()

for each_users_answers in all_answers.each():
    # For the first answer ->
    print("\n\n" + each_users_answers.val()['email'])

    answer = each_users_answers.val()['a1']
    result = givVal(model_answer1, keywords1, answer, out_of1)
    print("Marks : " + str(result))
    db.child("answers").child(each_users_answers.key()).update({"result1": result})

    # For the Second answer ->
    answer = each_users_answers.val()['a2']
    result = givVal(model_answer2, keywords2, answer, out_of2)
    print("Marks : " + str(result))
    db.child("answers").child(each_users_answers.key()).update({"result2": result})

    # For the third answer ->
    answer = each_users_answers.val()['a3']
    result = givVal(model_answer3, keywords3, answer, out_of3)
    print("Marks : " + str(result))
    db.child("answers").child(each_users_answers.key()).update({"result3": result})

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



