# coding=utf-8
from django import forms
from django.core.exceptions import ValidationError

from .models import Competicio


class CompeticioForm(forms.ModelForm):

    class Meta:
        model = Competicio
        fields = ('text', 'imatge',)

    def clean_text(self):

        nou_text = self.cleaned_data.get('text')
        ja_existeix = Competicio.objects.filter(text=nou_text).count()

        if ja_existeix > 0:
            raise ValidationError("Competició ja existent.")

        return self.cleaned_data.get('text', '')
