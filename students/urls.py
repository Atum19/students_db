
from django.conf.urls import include, url
from django.contrib import admin
import debug_toolbar   # add this
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView, TemplateView

from views import students, groups, exams, contact_admin, journal
# from students import views

urlpatterns = [
    # Students urls
    # url(r'^$', views.students_list, name='home'),
    url(r'^__debug__/', include(debug_toolbar.urls)),   # added this line

    url(r'^$', students.students_list, name='home'),
    url(r'^students/$', students.students_list, name='home'),
    # url(r'^students/add/$', students.students_add, name='students_add'),
    url(r'^students/add_form/$', students.StudentAddView.as_view(), name='students_add'),

    url(r'^students/(?P<pk>\d+)/edit/$', students.StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', students.StudentDeleteView.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    url(r'^groups/add/$', groups.groups_add, name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete, name='groups_delete'),

    # Exams urls
    url(r'^exams/$', exams.exams_list, name='exams'),
    url(r'^exams/add/$', exams.exams_add, name='exams_add'),
    url(r'^exams/(?P<eid>\d+)/edit/$', exams.exams_edit, name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete/$', exams.exams_delete, name='exams_delete'),

    # Journal urls
    # url(r'^journal/$', journal.JournalView.as_view(), name='journal'),
    url(r'^journal/(?P<pk>\d+)?/?$', journal.JournalView.as_view(), name='journal'),

    # User Related urls
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name=' home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    # Contact Admin Form
    # url(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),
    url(r'^contact-admin/$', contact_admin.ContactView.as_view(), name='contact_admin'),
]
