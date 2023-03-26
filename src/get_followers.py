# import the module
import json
import os
import tweepy, requests
from dotenv import load_dotenv

load_dotenv()

# assign the values accordingly
consumer_key = os.getenv('APIKey')
consumer_secret = os.getenv('APIKeySecret')
access_token = os.getenv('AccessToken')
access_token_secret = os.getenv('AccessTokenSecret')
bearer_token = os.getenv('BearerToken')

headers = {"Authorization": "Bearer {}".format(bearer_token)}

# authorization of consumer key and consumer secret

def use_tweepy():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    screen_name = "folorunso__"

    current_cursor=-1
    followers_batch = api.get_followers(screen_name=screen_name, count=200, cursor=current_cursor)
    followers = [follower._json for follower in followers]
    print (json.dumps(followers))


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params=None):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
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


def main():
    user_id = get_user_id('folorunso__')
    next_token = None
    json_data = []
    while next_token or next_token is None:
        url =  "https://api.twitter.com/2/users/{}/followers".format(user_id)
        params = {"max_results": 100, "pagination_token": next_token}
        json_response = connect_to_endpoint(url, params)
        json_data.extend(json_response['data'])
        try:
            next_token = json_response['meta']['next_token']
        except KeyError:
            break
    
    print(json.dumps(json_data))


if __name__ == "__main__":
    main()


