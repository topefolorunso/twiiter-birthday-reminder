import json
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession



def scrape_user_profile(username):
    session = HTMLSession()
    url = "https://twitter.com/{}".format(username)
    r = session.get(url)
    return r

def parse_user_profile(response):
    response.html.render(wait = 10)
    birthday_xpath = "//span[@data-testid='UserBirthdate']"
    birthdays = response.html.xpath(birthday_xpath)
    birthday_texts = [
        birthday.text for birthday in birthdays
        ]
    return birthday_texts[0] if len(birthday_texts) else None 


def get_user_birthday(username):
    response = scrape_user_profile(username)
    birthday_text = parse_user_profile(response)

    try:
        birthday = birthday_text \
            .replace('Born ', '') \
                .split()
        return birthday

    except AttributeError:
        return None


followers = [{
        "id": "2382418134",
        "name": "omotosho",
        "username": "toshiey_lz"
    },
    {
        "id": "1518491347245801472",
        "name": "Tijo",
        "username": "temiakanmode"
    },
    {
        "id": "199206734",
        "name": "Vally B",
        "username": "Vall_erie"
    }]

followers_usernames = [
    follower.get('username') 
    for follower in followers
    ]

followers_birthdays = [
    get_user_birthday(username) 
    for username in followers_usernames
    ]

print(followers_birthdays)
