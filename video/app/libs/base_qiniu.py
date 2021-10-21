# coding: utf-8

from qiniu import Auth, put_data, put_file
from config import settings


class Qiniu(object):


    def __init__(self, bucket_name, base_url):
        self.bucket_name = bucket_name
        self.base_url = base_url
        self.q = Auth(settings.QINIU_AK, settings.QINIU_SK)

    # 将文件存入七牛云服务器
    def put(self, name, path):
        token = self.q.upload_token(self.bucket_name, name)
        ret, info = put_file(token, name, path)
        print('ret:', ret)
        print('info', info)

        if 'key' in ret:
            remote_url = "http://" + self.base_url + '/' + ret['key']
            print('remote_url:',remote_url)
            return remote_url


qiniu_video = Qiniu(bucket_name=settings.QINIU_VIDEO,
                    base_url=settings.QINIU_VIDEO_URL)