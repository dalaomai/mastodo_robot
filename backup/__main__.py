import settings
from utils import cos_clinet

cos_clinet.upload_file(
    Bucket=settings.COS_BUCKET,
    LocalFilePath='.temp/7dd42f11ly1gwlf88k2jtg207i07i1l0.gif',
    Key='1.gif'
)
