# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..util import paginate
from ..models.groups import Group


# Views for Groups
def groups_list(request):
    groups = Group.objects.all()

    # try to order groups list
    order_by = request.GET.get('order_by', '')
    # order_by = request.GET.get('order_by')
    # print '>>>>>>>>>', order_by
    if order_by in ('title',):
        # print 222222222
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            # if request.GET.get('reverse') == '1':
            groups = groups.reverse()

    # # paginate students
    # paginator = Paginator(groups, 3)
    # page = request.GET.get('page')
    # try:
    #     groups = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     groups = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver
    #     # last page of results.
    #     groups = paginator.page(paginator.num_pages)

    context = paginate(groups, 2, request, {}, var_name='groups')
    return render(request, 'students/groups_list.html', context)


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
