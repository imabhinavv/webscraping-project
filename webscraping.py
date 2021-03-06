import requests
import random
from bs4 import BeautifulSoup
from csv import DictReader

base_url="http://quotes.toscrape.com"
def read_quotes(filename):
    with open(filename,"r") as file:
        csv_reader=DictReader(file)
        return list(csv_reader) 

def start_game  (quotes):
    quote= random.choice(quotes)
    remaining_guesses=4
    print("Here is a quote")
    print(quote["text"])
    guess=''
    while guess.lower()!=quote["author"].lower() and remaining_guesses>0:
        guess=input(f"Who said this quote? Guesses remaining: {remaining_guesses}")
        if guess.lower()==quote["author"].lower():
            print("You got it")
            break
        remaining_guesses-=1
        if remaining_guesses==3:
            res=requests.get(f"{base_url}{quote['bio-link']}")
            soup=BeautifulSoup(res.text,"html.parser")
            birth_date=soup.find(class_="author-born-date").get_text()
            birth_location=soup.find(class_="author-born-location").get_text()
            print(f"Here is a hint: The author was born on {birth_date} {birth_location}")
        elif remaining_guesses==2:
            print(f"Author first name starts with:{quote['author'][0]}")
        elif remaining_guesses==1:
            last_name=quote["author"].split(" ")[1][0]
            print(f"Author last name starts with:{last_name}")
        else:
            print(f"you are out of guesses. The answer is{quote['author']}")

    again=''
    while again.lower() not in ('y','yes','n','no'):
        again=input("would you like to play again(y/n)?")
    if again.lower() in ('yes','y'):
        return start_game(quotes)
    else:
        print("ok goodbye")
quotes=read_quotes("quptes.csv")
start_game(quotes)
    
            
