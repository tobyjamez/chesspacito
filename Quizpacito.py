import requests
import json 
import random
#categories
#9= General knowledge
#10=Entertainment:Books
#11=Entertainment:Film
#12=Entertainment:Music
#13=Entertainment:Musicals & Theater
#14=Entertainment:Television
#15=Entertainment:Video Games
#16=Entertainment:Board Games
#17= Science & Nature
#18=Science:Computers
#19=Science:Mathematics
#20=Mythology
#21=Sport
#22=Geography
#23=History
#24=Politics
#25=Art
#26=Celebrities
#27=Animals
#28=Vehicles
#29=Entertainment:Comics
#30=Science:Gadgets
#31=Entertainment:Japanese Anime & Manga
#32=Entertainment:Cartoons & Animations




def get_quiz(category,diff):
    r = requests.get("https://opentdb.com/api.php?amount=10&category="+category+"&difficulty="+diff+"&type=multiple")
    return r.json()




def make_quiz(category,diff):
    q = get_quiz(category,diff)
    score = 0
    print('Please answer only with 1,2,3 or 4 \n')
    for i in range(len(q['results'])):
        correct = q['results'][i]['correct_answer']
        incorrect1=q['results'][i]['incorrect_answers'][0]
        incorrect2=q['results'][i]['incorrect_answers'][1]
        incorrect3=q['results'][i]['incorrect_answers'][2]
        possible = [correct,incorrect1,incorrect2,incorrect3]
        random.shuffle(possible)
        print(q['results'][i]['question']+'\n %s   %s   %s   %s' %tuple(possible))
        answer = possible[int(input())-1]
        if answer == correct:
            score +=1
        while answer != correct and answer != incorrect1 and answer != incorrect2 and answer != incorrect3:
            print('Please enter valid answer')
            answer = possible[int(input())-1]
    print('\n Your score: ' + str(score))
    
    
    
    
q = make_quiz("17",'easy')