from django import forms
from .models import *
from django.forms.widgets import DateInput, TextInput


class AddChalanForm(forms.ModelForm):
    class Meta:
        model = Chalan
        exclude = ('owner',)
        widgets = {
            'product': TextInput(attrs={'class': 'input', 'placeholder': 'SElect Product', }),
            'quantity': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            # 'unit': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            'imported_from': TextInput(attrs={'class': 'input', 'placeholder': 'USA'}),
            'import_date': DateInput(attrs={'class': 'input', 'placeholder': 'mm/dd/yyyy'}),
        }
