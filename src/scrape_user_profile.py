from .database.mongo import get_mongodb_collection
from .util.helper_functions import get_or_create_new_user, scrape_user_profile



def main(username):

    user_id = get_or_create_new_user(username= username)

    birthday = scrape_user_profile(username)
    birthday_details = {
        'birth_month': birthday[0],
        'birth_day': birthday[1]
    }

    users_collection = get_mongodb_collection("users")
    users_collection.update_one(
        {'user_id': user_id},
        { "$set": birthday_details }
    )

    return True
    

if __name__ == "__main__":
    username = 'folorunso__'
    main(username= username)
