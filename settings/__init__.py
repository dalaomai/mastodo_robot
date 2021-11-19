import environs

env = environs.Env()
env.read_env()


MASTODON_ACCESS_TOKEN = env.str('MASTODON_ACCESS_TOKEN')
MASTODON_API_BASE_URL = env.str(
    'MASTODON_API_BASE_URL', 'https://mastodon.dalaomai.cn/')
