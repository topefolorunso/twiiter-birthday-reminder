from src import get_followers, scrape_user_profile

username = 'folorunso__'

try:
    print('onboarding {}...'.format(username))
    get_followers.main(username)
    scrape_user_profile.main(username)

except Exception as e:
    print(e)