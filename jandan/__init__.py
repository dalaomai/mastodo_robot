import os
import random
import time
import urllib
from http import HTTPStatus
from urllib.parse import urlparse

import requests
from lxml import etree

from mastd import mastodon_client
from utils import logger

JIANDAN_PIC_HOST = 'https://jandan.net/pic'


def get_pic(url=JIANDAN_PIC_HOST):
    rsp = requests.get(url)
    if rsp.status_code != HTTPStatus.OK:
        return None

    html = etree.HTML(rsp.text)

    comments = html.xpath('/html/body/div/div[2]/div[1]/div[2]/ol/li')

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


def download_img(uri, fileFolder='.temp'):

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
    return mastodon_client.media_post(filepath)


comment_latest_id = -1


def crawling_jiandan():
    global comment_latest_id

    while True:
        for i in get_pic():
            comment_id, text, imgs = i
            if comment_id <= comment_latest_id:
                continue

            img_ids = []
            for url in imgs:
                media_id = media_post_to_matodon(url).get('id')
                if media_id:
                    img_ids.append(media_id)

            text = f'#煎蛋 #无聊图 http://jandan.net/t/{comment_id} \n{text}'
            mastodon_client.status_post(text, media_ids=img_ids)
            comment_latest_id = comment_id
            logger.info(f'send {comment_id}')

        time.sleep(random.randint(20, 30))


if __name__ == "__main__":
    crawling_jiandan()
