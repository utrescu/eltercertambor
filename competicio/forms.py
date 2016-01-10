from django import forms

from .models import Competicio


class CompeticioForm(forms.ModelForm):

        class Meta:
            model = Competicio
            fields = ('text', 'imatge',)

