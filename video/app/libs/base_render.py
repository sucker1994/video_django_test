# coding:utf-8

from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse

def render_to_response(request, templates, data=None):
    context_instance = RequestContext(request)
    path = settings.TEMPLATES[0]['DIRS'][0]

    print('模板路径：{}'.format(path))
    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )

    mako_templates = lookup.get_template(templates)

    if not data:
        data = {}

    if context_instance:
        context_instance.update(data)

    result = {}

    for d in context_instance:
        result.update(d)

    result['request'] = request
    print('request.META:',request.META.get('CSRF_COOKIE'),'++++++++')
    result['csrf_token'] = '<input type="hidden" name="csrfmiddlewaretoken" ' \
                           'value={0}>'.format(request.META.get('CSRF_COOKIE'))

    print('csrf_token:{}'.format(data['csrf_token']))
    return HttpResponse(mako_templates.render(**result))