# coding:utf-8

from config import settings
import os
import time
import shutil
from app.libs.base_qiniu import qiniu_video
from app.model.video import Video, VideoSub


def check_and_get_videotype(type_obj, type_value, message):
    try:
        final_type_obj = type_obj(type_value)
    except:
        return {'code':-1, 'msg':message}

    return {'code':0,'msg':'success','data':final_type_obj}


def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


def handle_video(url_file, video_id, number):
    """

    :param url_file: 传入的视频路径
    :param video_id: 视频的id
    :param number: 当前视频的集数
    :return: 返回True或者False
    """

    in_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp')
    out_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_out')

    name = '{}_{}'.format(int(time.time()), url_file.name)

    # 文件路径名称
    file_path = '/'.join([in_path, name])

    temp_path = url_file.temporary_file_path()

    shutil.copyfile(temp_path, file_path)
    out_name = '{}_{}'.format(int(time.time()), url_file.name.split('.')[0])

    out_path = '/'.join([out_path, out_name])
    print('file_path:', file_path)
    print('out_path', out_path)
    command = "ffmpeg -i {} -c copy {}.mp4".format(file_path, out_path)
    print('cmd:', command)
    print("执行ffmpeg")
    os.system(command)

    out_name = '.'.join([out_path, 'mp4'])

    if not os.path.exists(out_name):
        print('out_name不存在')
        remove_path([out_name, out_path])
        return False

    url = qiniu_video.put(url_file.name, out_name)
    print('url:', url)


    if url:
        print('将视频url存入videosub中:{}'.format(url))
        video = Video.objects.get(pk=video_id)

        try:
            VideoSub.objects.create(
                video=video,
                url=url,
                number=number
                )
            print('true')
            return True
        except:
            print('false')
            return False
        finally:
            remove_path([out_name, out_path])
    remove_path([out_name, out_path])
    return False

