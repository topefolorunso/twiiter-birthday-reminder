# import the module
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# assign the values accordingly
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


def main():
    user_id = get_user_id('folorunso__')
    next_token = None
    json_data = []
    while next_token or next_token is None:
        next_100_followers, next_token = get_100_followers(user_id, next_token)
        json_data.extend(next_100_followers)
    
    return json_data
    print(json.dumps(json_data))


if __name__ == "__main__":
    print(main())


