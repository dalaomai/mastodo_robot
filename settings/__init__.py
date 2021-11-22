import environs

env = environs.Env()
env.read_env()


MASTODON_ACCESS_TOKEN = env.str('MASTODON_ACCESS_TOKEN')
MASTODON_API_BASE_URL = env.str(
    'MASTODON_API_BASE_URL', 'https://mastodon.dalaomai.cn/')


TENCENT_CLOUD_ID = env.str('TENCENT_CLOUD_ID')
TENCENT_CLOUD_key = env.str('TENCENT_CLOUD_key')

COS_BUCKET = 'mastodon-backup-1252550862'
