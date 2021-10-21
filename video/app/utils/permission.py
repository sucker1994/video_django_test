# coding:utf-8

import functools
from django.shortcuts import reverse, redirect

def dashboard_auth(func):

    @functools.wraps(func)
    def wraper(self, request, *args, **kwargs):

        user = request.user

        if not user.is_authenticated or not user.is_superuser:
            print(111)
            return redirect('{}?to={}'.format(reverse('login'), request.path))

        return func(self, request, *args, **kwargs)

    return wraper

