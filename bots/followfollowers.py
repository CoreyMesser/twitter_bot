import tweepy
import logging
from bots.config import create_api
import time

from bots.constants import Constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

con = Constants()

def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()

def check_friend(api,user):
    status = api.show_friendship(user)
    return status['relationship']['source']['following']

def make_friend(api, user):
    api.create_friendship(screen_name=user)

def update_friend(api, user):
    api.create_mute(screen_name=user)
    api.add_list_member(list_id=con.LIST_ID, screen_name=user)

def get_user_list():
    # gets list from db
    sql = """
    SELECT artists FROM public.artists WHERE artist_twitter not like 'None'
    """
def main():
    api = create_api()
    while True:
        follow_followers(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
