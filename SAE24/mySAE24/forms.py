from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models
from django import forms

class Test1(ModelForm):
    class Meta:
        model = models.test1
        fields = ('OKAY')
        labels = {
            'OKAY' : _('OKAY'),
            }


class Test2(ModelForm):
    class Meta:
        model = models.test2
        fields = ('OUHO')
        labels = {
            'OUHO' : _('ouho'),
        }