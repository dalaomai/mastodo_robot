import datetime
import os
import random
import time
from http import HTTPStatus
from urllib.parse import urlparse

import requests
from dateutil.tz import tzutc
from lxml import etree
from mastodon.Mastodon import MastodonError

from mastd import mastodon_client
from utils import logger

JIANDAN_PIC_HOST = 'https://jandan.net/pic'


def get_pic(url=JIANDAN_PIC_HOST):
    comment_xpath = '/html/body/div/div[2]/div[1]/div[2]/ol/li'

    rsp = requests.get(url)
    if rsp.status_code != HTTPStatus.OK:
        return None
    html_pic = etree.HTML(rsp.text)

    older_comment = html_pic.xpath('//*[@title="Older Comments"]')[0]
    rsp = requests.get(f"https:{older_comment.attrib['href']}")
    if rsp.status_code != HTTPStatus.OK:
        return None
    html_older = etree.HTML(rsp.text)

    comments = html_pic.xpath(comment_xpath) + html_older.xpath(comment_xpath)

    result = []
    for comment in comments:
        comment_id = ''.join(filter(str.isdigit, comment.attrib.get('id', '')))
        if not comment_id:
            continue
        comment_id = int(comment_id)

        comment_p = comment.xpath('div/div/div[@class="text"]/p')
        if not comment_p:
            continue
        comment_p = comment_p[0]

        imgs = set()
        for comment_p_c in comment_p.getchildren():
            if comment_p_c.tag == 'a':
                img = comment_p_c.attrib.get('href', None)
                if img:
                    imgs.add(f'https:{img}')
        result.append(
            (comment_id, comment_p.text, imgs)
        )

    if result:
        result = list(sorted(result, key=lambda x: x[0]))
    return result


def download_img(uri, fileFolder='.temp/media'):
    os.makedirs(fileFolder, exist_ok=True)
    filename = urlparse(uri).path.split('/')[-1]

    full_filepath = os.path.join(fileFolder, filename)

    with open(full_filepath, 'wb') as f:
        r = requests.get(uri, stream=True)
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
    return full_filepath


def media_post_to_matodon(url):
    filepath = download_img(url)
    try:
        info = mastodon_client.media_post(filepath)
    except MastodonError as e:
        logger.exception(f'upload {url} error')
        raise e
    finally:
        os.remove(filepath)
    return info


comment_latest_id = -1


def clear_toot():
    del_time = datetime.datetime.now().replace(tzinfo=tzutc()) - \
        datetime.timedelta(days=7)

    while True:
        toots = mastodon_client.timeline_hashtag('煎蛋', limit=100)
        if not toots:
            break

        for toot in toots:
            id = toot['id']
            created_at = toot['created_at']
            if(created_at < del_time):
                mastodon_client.status_delete(id)
            print(f'del {id}')


def crawling_jiandan():
    global comment_latest_id

    while True:
        try:
            for i in get_pic():
                comment_id, text, imgs = i
                text = text if text else ''

                if comment_id <= comment_latest_id:
                    continue

                img_ids = []
                for url in imgs:
                    try:
                        img_ids.append(media_post_to_matodon(url)['id'])
                    except Exception:
                        logger.exception('post media to matodon faile')
                        text += f'\n{url}'

                text = f'#煎蛋 #无聊图 http://jandan.net/t/{comment_id} \n{text}'

                try:
                    mastodon_client.status_post(text, media_ids=img_ids)
                except Exception:
                    logger.exception('send toot err')

                comment_latest_id = comment_id
                logger.info(f'send toot success: {comment_id}')
        except Exception:
            logger.exception('err: get jandan err')

        time.sleep(random.randint(40, 50))


if __name__ == "__main__":
    crawling_jiandan()
