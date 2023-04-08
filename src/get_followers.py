from .database.mongo import get_mongodb_collection
from .util.helper_functions import (get_or_create_new_user, get_100_followers)



def main(username: str):

    print('retreiving user id ...')
    user_id = get_or_create_new_user(username= username)
    
    print('getting followers list ...')
    next_token = None
    followers_list = []
    while next_token or next_token is None:
        next_100_followers, next_token = get_100_followers(user_id, next_token)
        followers_list.extend(next_100_followers)
        print('100 followers added ...')

    followers_list = [{
            "user_id": follower['id'], 
            "username": follower['username']
            } 
            for follower in followers_list
        ]

    # followers_id = map(get_or_create_new_user, None, followers_list)
    print('adding followers to database ...')
    followers_id = [
        get_or_create_new_user(follower) 
            for follower in followers_list
        ]

    users_collection = get_mongodb_collection("users")
    print('updating user\'s followers list ...')
    users_collection.update_one(
        {'user_id': user_id},
        { "$set": { "followers_id": followers_id } }
    )

    return True



if __name__ == "__main__":
    username = 'folorunso__'
    main(username= username)
