# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, ButtonHolder, Button, HTML
from crispy_forms.bootstrap import FormActions, AppendedText

from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form button
        self.helper.add_input(
            Submit('send_button', u'Надіслати'))

    from_email = forms.EmailField(
        label=u"Ваша Емейл Адреса")

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2560,
        widget=forms.Textarea)

    def send_email(self):
        data = self.cleaned_data
        send_mail('[contact admin form] ' + data.get('subject'),
                  'From: ' + data.get('from_email') + '\n\n' + data.get('message'),
                  data.get('from_email'),
                  [ADMIN_EMAIL])


class ContactView(FormView):
    # template_name = 'contact_form.html'
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    success_url = 'contact_admin'

    def dispatch(self, *args, **kwargs):
        return super(ContactView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contact_admin')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
        """This method is called for valid data"""

        try:
            # send_mail(subject, message, from_email, [ADMIN_EMAIL])
            form.send_email()
        except Exception:
            message = _(u'Під час відправки листа виникла непередбачувана '
                        u'помилка. Спробуйте скористатись даною формою пізніше.')
            messages.info(self.request, message)
        else:
            message = _(u'Повідомлення успішно надіслане!')
            messages.success(self.request, message)

        # redirect to same contact page with success message
        return HttpResponseRedirect(reverse('contact_admin'))

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        message = _(u'Виникла непередбачувана помилка. '
                    u'Спробуйте скористатись даною формою пізніше.')
        messages.error(self.request, message)
        # print '>>>>>>> @@@@@@@@@@ #########', context
        # context['form'] = form
        # context[show_results] = False
        return self.render_to_response(context)
