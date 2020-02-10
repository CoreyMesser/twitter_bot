import tweepy
import logging
from app.config import create_api
from app.aws_services import AWSConnection
import time

from app.constants import Constants

from app.logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()

con = Constants()
awsc = AWSConnection()

def follow_followers(api):
    _log.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            _log.info(f"Following {follower.name}")
            follower.follow()


def validate_friend(api, user):
    try:
        api.show_friendship(target_screen_name=user)
        _log.info(f'{user} exists!')
        return True
    except Exception as e:
        _log.error(f"User {user} does not exist. Response {e}", exc_info=True)
        return False

def check_friend(api,user):
    status = api.show_friendship(target_screen_name=user)
    sta = status[0].following
    return sta


def make_friend(api, user):
    _log.info(f'Making {user} my friend')
    api.create_friendship(screen_name=user, follow=True)


def update_friend(api, user):
    _log.info(f'Muting {user}')
    api.create_mute(screen_name=user)

    _log.info(f'Adding {user} to list')
    api.add_list_member(list_id=con.LIST_ID, screen_name=user)


def get_user_list():
    latest = awsc.s3_get_latest()
    user_list = awsc.s3_get_csv_object(latest=latest)
    return user_list


def parse_user(user):
    return user.split('/')[-1]


def process_friends(api):
    _log.info('Starting the Friending...')
    user_list = get_user_list()
    _log.info('Potential friends aquired...')
    for user in user_list:
        friend = parse_user(user=user)
        _log.info(f'Checking {friend}')
        if validate_friend(api=api, user=friend):
            if check_friend(api=api, user=friend):
                _log.info(f'{friend} already my friend!')
                continue
            else:
                make_friend(api=api, user=friend)
                update_friend(api=api, user=friend)
        else:
            _log.info(f'{friend} does not exist!')


def main():
    api = create_api()
    process_friends(api=api)
    _log.info("FIN the Friending")

if __name__ == "__main__":
    main()
