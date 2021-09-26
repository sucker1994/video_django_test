# coding:utf-8

from django.views.generic import View
from app.libs.base_render import render_to_response

class Index(View):
    TEMPLATES = "dashboard/index.html"

    print('已经到达业务代码')
    def get(self, request):

        return render_to_response(request, self.TEMPLATES)