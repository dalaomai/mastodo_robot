import environs

env = environs.Env()
env.read_env()


MASTODON_ACCESS_TOKEN = env.str('MASTODON_ACCESS_TOKEN')
MASTODON_API_BASE_URL = env.str(
    'MASTODON_API_BASE_URL', 'https://mastodon.dalaomai.cn/')


TENCENT_CLOUD_ID = 'AKIDObaIjdGchV3KJ1ScV7RVIo32kAJBm69v'
TENCENT_CLOUD_key = 'XnlSt2vXswjESP5UcT3MO8cplBKCn69u'

COS_BUCKET = 'mastodon-backup-1252550862'
