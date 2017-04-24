# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Exam(models.Model):
    """Student Model"""

    class Meta(object):
        verbose_name = u"Екзамени"
        verbose_name_plural = u"Екзамени"

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва Предмету")

    data_exam = models.DateField(
        blank=False,
        verbose_name=u"Дата і час проведення",
        null=True)

    professor = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім'я викладача")

    # middle_name = models.CharField(
    #     max_length=256,
    #     blank=True,
    #     verbose_name=u"По-батькові",
    #     default='')

    # photo = models.ImageField(
    #     blank=True,
    #     verbose_name=u"Фото",
    #     null=True)
    #
    # ticket = models.CharField(
    #     max_length=256,
    #     blank=False,
    #     verbose_name=u"Білет")
    #
    # notes = models.TextField(
    #     blank=True,
    #     verbose_name=u"Додаткові нотатки")

    exam_group = models.ManyToManyField('Group',
                                        verbose_name=u"Група")
                                        # blank=True)
                                        # null=True)

    def __unicode__(self):
        if self.exam_group:
            return u"%s %s %s %s" % (self.name,
                                     self.data_exam,
                                     self.professor,
                                     ", ".join(self.exam_group.values_list('title', flat=True)))
        else:
            return u"%s %s %s" % (self.name,
                                  self.data_exam,
                                  self.professor)
