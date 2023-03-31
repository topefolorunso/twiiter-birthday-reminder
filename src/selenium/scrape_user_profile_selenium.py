from selenium.twitter_browser import TwitterBrowser



def scrape_user_profile(username):
    url = "https://twitter.com/{}".format(username)
    user_browser = TwitterBrowser(url=url)
    birthday_text = user_browser.get_user_birthday()

    try:
        birthday = birthday_text \
            .replace('Born ', '') \
                .split()
        return birthday

    except AttributeError:
        return None
    
    finally:
        user_browser.close()

# followers = [{
#         "id": "2382418134",
#         "name": "omotosho",
#         "username": "toshiey_lz"
#     },
#     {
#         "id": "1518491347245801472",
#         "name": "Tijo",
#         "username": "temiakanmode"
#     },
#     {
#         "id": "199206734",
#         "name": "Vally B",
#         "username": "Vall_erie"
#     }]

# followers_usernames = [
#     follower.get('username') 
#     for follower in followers
#     ]

# followers_birthdays = [
#     get_user_birthday(username) 
#     for username in followers_usernames
#     ]

# print(followers_birthdays)

username = "Vall_erie"
bday = scrape_user_profile(username)
print(bday)