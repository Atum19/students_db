# -*- coding: utf-8 -*-

from PIL import Image
from datetime import datetime

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.safestring import mark_safe
from django.forms import ClearableFileInput
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, HTML

from ..models.groups import Group
from ..models.students import Student


# Views for Students
def students_list(request):
	students = Student.objects.all()

	# try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()

	# paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		students = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver
		# last page of results.
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html',
                  {'students': students})


##########################################################################
# stud_add
# crispy


class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(StudentAddForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('students_add')
        # self.helper.form_action = reverse('students_dj_form')

        # twitter bootstrap styles
        self.helper.html5_required = True
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-4'

        self.helper.layout = Layout(
            Fieldset('', 'first_name', 'last_name', 'middle_name',
                     AppendedText('birthday', '<span class="glyphicon glyphicon-calendar"></span>'),
                     'photo', 'ticket', 'student_group', 'notes'))

        # add buttons
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link", formnovalidate='formnovalidate')
        ))

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            try:
                im = Image.open(photo)
                im.verify()
                im_size = im.size
                if (im_size[0] * im_size[1]) > 26214400:
                    raise ValidationError(u'Розмір файлу не повинен перевищувати 2 Мб',
                                          code='invalid')
            except Exception:
                raise ValidationError(u'Введіть коректний формат фото',
                                      code='invalid')
            return self.cleaned_data['photo']


class StudentAddView(FormView):
    model = Student
    template_name = 'students/students_dj_form.html'
    form_class = StudentAddForm
    success_url = 'home'

    def get_context_data(self, **kwargs):
        context = super(StudentAddView, self).get_context_data(**kwargs)
        context['title'] = _(u'Student add')
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування студента відмінено!' % reverse('home'))

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        """This method is called for valid data"""

        try:
            form.save()
        except Exception as e:
            messages.error(self.request, e)
        else:
            messages.success(self.request, u'Студента успішно додано!')
        # redirect to same contact page with success message
        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        message = _(u'Виникла непередбачувана помилка.')
        messages.error(self.request, message)
        return self.render_to_response(context)   # back to the same page

################################################################

################################################################
# update form


class StudentUpdateForm(StudentAddForm):
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})

"""

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-4'

        # add buttons
        self.helper.layout = Layout(
            Fieldset('', 'first_name', 'last_name', 'middle_name',
                 AppendedText('birthday', '<span class="glyphicon glyphicon-calendar"></span>'),
                              'photo', 'ticket', 'student_group', 'notes'),
            FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                # HTML(u"<a class='btn btn-link' href='%s'>%s</a>" % (reverse('home'), u'Cancel'))
                Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
            ))

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            try:
                im = Image.open(photo)
                im.verify()
                im_size = im.size
                if (im_size[0] * im_size[1]) > 26214400:
                    raise ValidationError(u'Розмір файлу не повинен перевищувати 2 Мб',
                                          code='invalid')
            except Exception:
                raise ValidationError(u'Введіть коректний формат фото',
                                      code='invalid')
            return self.cleaned_data['photo']
"""


class StudentUpdateView(UpdateView):
    model = Student
    # template_name = 'students/students_edit.html'
    template_name = 'students/students_dj_form.html'
    form_class = StudentUpdateForm
    # success_message = u'Student "%(first_name)s %(last_name)s" successfully saved!'

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Student Update')
        return context

    def get_success_url(self):
        return reverse('home')

        # def post(self, request, *args, **kwargs):
        # if request.POST.get('cancel_button'):
        #     message = _(u'Редагування студента відмінено!')
        #     messages.info(request, message)
        #     return HttpResponseRedirect(reverse('home'))
        # else:
        #     return super(StudentUpdateView, self).post(request, *args, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        message = _(u'Виникла непередбачувана помилка.')
        messages.error(self.request, message)
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        """Check if student is leader in any group.
        If yes, then ensure it's the same as selected group.
        """
        # get group where current student is a leader
        context = self.get_context_data(**kwargs)
        group = Group.objects.filter(leader=self.object.id)
        if group and form.cleaned_data['student_group'] != group:
            message = _(u'Студент є старостою групи %s.' % group.values()[0]['title'])
            messages.info(self.request, message)
            return self.render_to_response(context)
        else:
            message = _(u'Студента успішно збережено!')
            messages.success(self.request, message)
            return super(StudentUpdateView, self).form_valid(form)

#################################################################################

#################################################################################
# delete form


class StudentDeleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(StudentDeleteForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('students_delete',
                                          kwargs={'pk': kwargs['initial']['pk']})
        self.helper.form_method = 'POST'
        self.helper.html5_required = True
        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout = Layout(
            HTML(u"<p>%s</p>" % _(u'Do you really want to delete student {{ object }}?')),
            ButtonHolder(Submit('submit_button', _(u'Delete'), css_class='btn-danger'),
                         Submit('cancel_button', _(u'Cancel'), css_class='btn-default')))


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_dj_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(StudentDeleteView, self).get_context_data(**kwargs)
        context['title'] = _(u'Delete Student')
        context['form'] = StudentDeleteForm(initial={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        # messages.info(self.request, u'Студента успішно видалено!')
        # return HttpResponseRedirect(reverse('students:home'))
        return u'%s?status_message=%s' % (reverse('home'), _(u'success'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, u'Видалення студента відмінено!')
            return HttpResponseRedirect(reverse('home'))
            # return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home'), _(u'Student deletion canceled!')))
        else:
            messages.info(request, u'Студента успішно видалено!')
            return super(StudentDeleteView, self).post(request, *args, **kwargs)
