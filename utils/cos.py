from qcloud_cos import CosConfig, CosS3Client

import settings

secret_id = settings.TENCENT_CLOUD_ID
secret_key = settings.TENCENT_CLOUD_key
region = 'ap-guangzhou'
token = None
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id,
                   SecretKey=secret_key, Token=token, Scheme=scheme)


cos_clinet = CosS3Client(config)
