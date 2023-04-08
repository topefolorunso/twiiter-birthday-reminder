import os

import requests
from dotenv import load_dotenv

from ..database.mongo import get_mongodb_collection
from .twitter_browser import TwitterBrowser



load_dotenv()

consumer_key = os.getenv('APIKey')
consumer_secret = os.getenv('APIKeySecret')
access_token = os.getenv('AccessToken')
access_token_secret = os.getenv('AccessTokenSecret')
bearer_token = os.getenv('BearerToken')

headers = {"Authorization": "Bearer {}".format(bearer_token)}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params=None):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user_id(screen_name):
    url = f'https://api.twitter.com/1.1/users/lookup.json?screen_name={screen_name}'
    json_response = connect_to_endpoint(url)
    return json_response[0]['id']


def get_100_followers(user_id, next_token):
    url =  "https://api.twitter.com/2/users/{}/followers".format(user_id)
    params = {"max_results": 100, "pagination_token": next_token}
    json_response = connect_to_endpoint(url, params)

    next_100_followers = json_response['data']
    try:
        next_token = json_response['meta']['next_token']
    except KeyError:
        next_token = False
    
    return next_100_followers, next_token


def get_or_create_new_user(username=None, user=None):

    if user:
        user_id = user['user_id']
        new_user = user
    else:
        user_id = get_user_id(username)
        new_user = {
            'user_id': user_id,
            'username': username
        }

    users_collection = get_mongodb_collection("users")
    if not users_collection.find({}, {'user_id': user_id}):
        print('adding user {} to database ...'.format(new_user['username']))
        users_collection.insert_one(new_user)

    return user_id


def scrape_user_profile(username):
    url = "https://twitter.com/{}".format(username)
    user_browser = TwitterBrowser(url=url)
    birthday_text = user_browser.get_user_birthday()

    try:
        if birthday_text:
            birthday = birthday_text \
                .replace('Born ', '')
            
            if birthday == birthday_text:
                raise Exception
            
            return birthday.split()

    except:
        print(f"Error: incorrect birthday text '{birthday_text}'")
        raise Exception
            
    finally:
        user_browser.close()

