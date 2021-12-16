import datetime
import time

import settings
from clearer import clear_daily_data, clear_jandan_toot
from utils import cos_clinet
from utils.zip import zip_folder


def backup(data_folder, key_root='backup'):

    now_time = datetime.datetime.now()
    zip_file_name = f'{now_time.strftime("%Y-%m-%d")}.zip'
    backup_zip_file = zip_folder(
        data_folder, zip_file_name)
    cos_clinet.upload_file(
        Bucket=settings.COS_BUCKET,
        LocalFilePath=backup_zip_file,
        Key=f'{key_root}/{zip_file_name}',
        PartSize=50,
        EnableMD5=True
    )


def backup_task():
    while True:
        if datetime.datetime.now().day == 1:
            clear_daily_data(days=0)
            backup(settings.MASTODON_DATA_FOLDER, key_root='mastodob_backup')
        time.sleep(60*60*24)
