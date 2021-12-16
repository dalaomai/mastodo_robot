import datetime
import os
import time

from dateutil.tz import tzutc

from mastd import mastodon_client
from utils import logger


def clear_jandan_toot(days=7):
    del_time = datetime.datetime.now().replace(tzinfo=tzutc()) - \
        datetime.timedelta(days=days)

    max_id = None
    while True:
        toots = mastodon_client.timeline_hashtag(
            '煎蛋', max_id=max_id, limit=40)
        # print(toots[0]['id'])
        if not toots:
            break

        for toot in toots:
            id = toot['id']
            created_at = toot['created_at']

            max_id = id
            if(created_at < del_time):
                # print(f'del {id}')
                mastodon_client.status_delete(id)


def clear_daily_data(days=7):
    '''
    docker exec -it mastodon_web bin/tootctl statuses remove
    docker exec -it mastodon_web bin/tootctl media remove-orphans
    docker exec -it mastodon_web bin/tootctl media remove --days=14
    '''
    os.system('docker exec -it mastodon_web bin/tootctl statuses remove')
    os.system('docker exec -it mastodon_web bin/tootctl media remove-orphans')
    os.system(
        f'docker exec -it mastodon_web bin/tootctl media remove --days={days}')


def clear_task():

    while True:
        now_time = datetime.datetime.now()
        if now_time.hour == 1 and now_time.day % 5 == 0:
            try:
                clear_jandan_toot()
            except Exception:
                logger.exception('clear toot err')

            try:
                clear_daily_data()
            except Exception:
                logger.exception('clear daily data err')

        time.sleep(60*60)


if __name__ == '__main__':
    clear_task()
