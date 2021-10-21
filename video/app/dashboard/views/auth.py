# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class Login(View):
    TEMPLATES = "dashboard/auth/login.html"


    def get(self, request):

        # 如果用户已经登录，就跳转到dashboard首页
        print('已经进入登录页面')
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        to = request.GET.get('to', '')

        print('---------------to:',to)
        data = {'error':'', 'to': to}
        return render_to_response(request, self.TEMPLATES, data=data)

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to', '')
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

        if to:
            print('跳转到登录之前的页面')
            return redirect(to)

        print('直接跳到主页')
        return redirect(reverse('dashboard_index'))

# 注销登录
class Logout(View):

    def get(self, request):
        print('要退出登录啦')
        logout(request)

        return redirect(reverse('login'))




class AdminManager(View):
    TEMPLATES = "dashboard/auth/admin.html"
    print(2222)
    @dashboard_auth
    def get(self, request):
        print(3333)
        users = User.objects.all()
        page = request.GET.get('page', 1)
        print('++++++++++++++request.GET:',request.GET,'+++++++++++++')
        p = Paginator(users,2)
        if int(page) <=1:
            page=1
        current_page = p.get_page(int(page)).object_list

        total_page = p.num_pages
        print('current_page:', current_page, 'page:', page, 'total_p')
        data = {'users':current_page, 'total_pages':total_page, 'page_num': int(page)}

        return render_to_response(request,self.TEMPLATES,data)


class UpdateAdminStatus(View):

    def get(self, request):

        status = request.GET.get('status', 'on')
        print('status:', status)

        _status = True if status=='on' else False

        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))



