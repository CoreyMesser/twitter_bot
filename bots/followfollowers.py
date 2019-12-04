import tweepy
import logging
from bots.config import create_api
from bots.aws_services import AWSConnection as awsc
import time
import boto3

from bots.constants import Constants

logging.basicConfig(filename='twitlog.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

con = Constants()

def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()


def validate_friend(api, user):
    try:
        api.show_friendship(user)
        return True
    except Exception as e:
        logger.error(f"User {user} does not exist. Response {e}", exc_info=True)
        print(f"User {user} does not exist. Response {e}")
        return False

def check_friend(api,user):
    status = api.show_friendship(user)
    return status['relationship']['source']['following']


def make_friend(api, user):
    api.create_friendship(screen_name=user)


def update_friend(api, user):
    api.create_mute(screen_name=user)
    api.add_list_member(list_id=con.LIST_ID, screen_name=user)


def get_user_list():
    obj_list = awsc.s3_list_objects()
    latest = awsc.s3_get_latest(obj_list=obj_list)
    user_list = awsc.s3_get_csv_object(latest=latest)
    return user_list


def parse_user(user):
    return user.split('/')[-1]


def process_friends(api):
    logger.info('Starting the Friending...')
    user_list = get_user_list()
    logger.info('Potential friends aquired...')
    for user in user_list:
        friend = parse_user(user=user)
        logger.info(f'Checking {friend}')
        if validate_friend(api=api, user=friend):
            if check_friend(api=api, user=friend):
                logger.info(f'{friend} already my friend!')
                continue
            else:
                logger.info(f'Making {friend} my friend')
                make_friend(api=api, user=friend)
                logger.info(f'Muting {friend}')
                update_friend(api=api, user=friend)
        else:
            logger.info(f'{friend} does not exist!')


def main():
    api = create_api()
    while True:
        follow_followers(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
