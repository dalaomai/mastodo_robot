from mastodon import Mastodon

import settings

mastodon_client = Mastodon(
    access_token=settings.MASTODON_ACCESS_TOKEN,
    api_base_url=settings.MASTODON_API_BASE_URL)

# mastodon_client.toot("Test")
