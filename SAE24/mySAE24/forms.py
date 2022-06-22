from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models

class capteurForm(ModelForm):
    class Meta:
        model = models.capteur
        fields = ('nom', 'emplacement')
        labels = {
            'nom' : _('Nom'),
            'emplacement':_('Emplacement'),
        }