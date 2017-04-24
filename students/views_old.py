# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def students_list(request):
	students = (
		{'id': 1,
		'first_name': u'Віталій',
		'last_name': u'Подоба',
		'ticket': 235,
		'image': 'img/me.jpeg'},
		{'id': 2,
		'first_name': u'Корост',
		'last_name': u'Андрій',
		'ticket': 254,
		'image': 'img/piv.png'},
		{'id': 3,
		'first_name': u'Мельник',
		'last_name': u'Валентин',
		'ticket': 123,
		'image': 'img/podoba3.jpg'},
	)
	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Views for Groups
def groups_list(request):
	groups = (
		{'id': 1,
		'leader': {
			'id': 1,
			'name': u'Віталій Подоба',
		},
		'name': u'МтМ-21'},
		{'id': 2,
		'leader': {
			'id': 2,
			'name': u'Корост Андрій',
		},
		'name': u'МтІ-22'},
		{'id': 3,
		'leader': {
			'id': 3,
			'name': u'Мельник Валентин',
		},
		'name': u'МтС-23'}
	)
	return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)
