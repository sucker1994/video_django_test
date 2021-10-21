# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.video import VideoType, FromType, NationalityType, Video, VideoSub, IdentityType, VideoStar
from app.utils.common import check_and_get_videotype, handle_video



class ExternalVideo(View):
    TEMPLATES = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):

        error = request.GET.get('error','')
        data={'error': error}

        cus_videos = Video.objects.filter(from_to=FromType.custom.value)
        ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['ex_videos'] = ex_videos
        data['cus_videos'] = cus_videos

        return render_to_response(request, self.TEMPLATES, data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        nationality = request.POST.get('nationality')
        from_to = request.POST.get('from_to')
        video_type = request.POST.get('video_type')
        info = request.POST.get('info')
        video_id = request.POST.get('video_id')

        print('是否获取到video_id:', video_id )
        if video_id:
            reverse_path = reverse('video_update', kwargs={'video_id':video_id})
        else:
            reverse_path = reverse('external_video')



        if not all([name, image,nationality,from_to,video_type, info]):
            return redirect('{}?error={}'.format(reverse_path,'缺少必要字段'))

        result = check_and_get_videotype(VideoType, video_type, '非法视频类型')
        if result.get('code') != 0:

            return redirect('{}?error={}'.format(reverse_path,result['msg']))
        video_type_obj = result.get('data')

        result = check_and_get_videotype(FromType, from_to, '非法视频来源')
        if result.get('code') != 0:

            return redirect('{}?error={}'.format(reverse_path,result['msg']))
        from_type_obj = result.get('data')

        result = check_and_get_videotype(NationalityType, nationality, '非法视频国籍')
        if result.get('code') != 0:

            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        nationality_obj = result.get('data')


        # 创建video表中数据
        # print('开始创建video表的内容啦。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。')
        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=video_type,
                    from_to=from_to,
                    nationality=nationality,
                    info=info
                )
            except:
                return redirect('{}?error={}'.format(reverse_path, '创建失败'))

        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = image
                video.video_type=video_type
                video.from_to = from_to
                video.nationality = nationality
                video.info = info
                video.save()
            except:
                return redirect('{}?error={}'.format(reverse_path, '修改失败'))

        return redirect(reverse_path)


# 对视频的地址等进行处理
class VideoSubView(View):
    TEMPLATES = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        error = request.GET.get('error')
        data['error'] = error
        video = Video.objects.get(pk=video_id)
        print('data')


        data['video'] = video
        print('data：', data)

        return render_to_response(request, self.TEMPLATES, data)

    def post(self, request, video_id):


        number = request.POST.get('number')
        videosub_id = request.POST.get('videosub_id')

        video = Video.objects.get(pk=video_id)

        print(111)
        if FromType(video.from_to) == FromType.custom:
            url = request.FILES.get('url')
        else:
            url = request.POST.get('url')


        url_format = reverse('video_sub', kwargs={'video_id':video_id})

        print('videosub++++++++++++++++:', url, number, video_id)
        if not all([url, number]):
            return redirect('{}?error={}'.format(url_format, '缺少必要字段'))

        if FromType(video.from_to) == FromType.custom:
            print('如果视频是自知视频，处理自制视频')
            handle_video(url, video_id, number)

        if not videosub_id:
            try:
                VideoSub.objects.create(video=video, url=url, number=number)
            except:
                return redirect('{}?error={}'.format(url_format, '创建失败'))
        else:
            # 数据更新表操作
            video_sub = VideoSub.objects.get(pk=videosub_id)
            try:
                video_sub.url = url
                video_sub.number = number
                video_sub.save()

            except:
                return redirect('{}?error={}'.format(url_format, '修改失败'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoStarView(View):

    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        print('打印演员名称身份等信息', name, identity, video_id)

        if not all([name, identity, video_id]):
            print(1111)
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

        print(2222)
        result = check_and_get_videotype(IdentityType, identity, '非法身份类型')
        print('result:',result)
        if result.get('code') != 0:
            print(3333)
            return redirect('{}?error={}'.format(reverse('video_sub'), result['msg']))


        # 将表中中的数据提交到后台数据库
        video = Video.objects.get(pk=video_id)
        print('保存数据到后台')
        try:
            video = VideoStar.objects.create(
                video = video,
                name = name,
                identity = identity
            )
        except:
            return redirect('{}?error={}'.format(reverse('video_sub'), '创建失败'))


        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class StarDelete(View):

    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()

        return redirect(reverse('video_sub', kwargs={'video_id':video_id}))


class SubDelete(View):

    def get(self, request, videosub_id, video_id):
        print('跳到删除集数页面啦。。。。。。。。')
        VideoSub.objects.filter(id=videosub_id).delete()

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoUpdate(View):
    TEMPLATES = 'dashboard/video/video_update.html'

    @dashboard_auth
    def get(self, request, video_id):

        data = {}
        video = Video.objects.get(pk=video_id)
        data['video'] = video


        return render_to_response(request, self.TEMPLATES, data)


class VideoupdateStatus(View):

    def get(self, request, video_id):

        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()

        return redirect(reverse('external_video'))

