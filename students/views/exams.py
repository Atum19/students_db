# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.exams import Exam


# Views for Exams
def exams_list(request):
	exams = Exam.objects.all()
	print '>>>>>>>>>', exams
	# try to order groups list
	# order_by = request.GET.get('order_by', '')
	# # order_by = request.GET.get('order_by')
	# print '>>>>>>>>>', order_by
	# if order_by in ('title',):
	# 	print 222222222
	# 	groups = groups.order_by(order_by)
	# 	if request.GET.get('reverse', '') == '1':
	# 	# if request.GET.get('reverse') == '1':
	# 		groups = groups.reverse()
    #
	# # paginate students
	# paginator = Paginator(groups, 2)
	# page = request.GET.get('page')
	# try:
	# 	students = paginator.page(page)
	# except PageNotAnInteger:
	# 	# If page is not an integer, deliver first page.
	# 	students = paginator.page(1)
	# except EmptyPage:
	# 	# If page is out of range (e.g. 9999), deliver
	# 	# last page of results.
	# 	students = paginator.page(paginator.num_pages)

	return render(request, 'students/exam_schedule.html', {'exams': exams})

def exams_add(request):
	return HttpResponse('<h1>Exam Add Form</h1>')

def exams_edit(request, eid):
	return HttpResponse('<h1>Edit Exam %s</h1>' % eid)

def exams_delete(request, eid):
	return HttpResponse('<h1>Delete Exam %s</h1>' % eid)
