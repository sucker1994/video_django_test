# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from app.libs.base_render import render_to_response

class Login(View):
    TEMPLATES = "dashboard/auth/login.html"


    def get(self, request):

        # 如果用户已经登录，就跳转到dashboard首页
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        data = {'error':''}
        return render_to_response(request, self.TEMPLATES, data=data)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        data={}
        print(username, password)

        data['error'] = '不存在该用户'
        #验证用户是否已经注册
        exists = User.objects.filter(username=username).exists()
        if not exists:
            return render_to_response(request, self.TEMPLATES, data=data)
        # 验证用户名是否和密码匹配
        user = authenticate(username=username, password=password)
        if not user:
            data['error']='密码不正确'
            return render_to_response(request, self.TEMPLATES, data=data)

        if not user.is_superuser:
            data['error']= '您无权登录'
            return render_to_response(request, self.TEMPLATES, data=data)

        login(request,user)

        return redirect(reverse('dashboard_index'))

# 注销登录
class Logout(View):

    def get(self, request):
        print('要退出登录啦')
        logout(request)

        return redirect(reverse('dashboard_login'))




class AdminManager(View):
    TEMPLATES = "dashboard/auth/admin.html"

    def get(self,request):
        data={}
        users = User.objects.all()
        data['users'] = users
        print(users)
        return render_to_response(request,self.TEMPLATES,data)


class UpdateAdminStatus(View):

    def get(self, request):

        status = request.GET.get('status', 'on')

        _status = True if status=='on' else False

        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))



