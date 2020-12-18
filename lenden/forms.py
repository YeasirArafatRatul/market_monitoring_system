from .models import *
from django.forms.widgets import DateInput, TextInput

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Institute Name', }),
            'quantity': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            # 'unit': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            'imported_from': TextInput(attrs={'class': 'input', 'placeholder': 'USA'}),
            'import_date': DateInput(attrs={'class': 'input', 'placeholder': 'mm/dd/yyyy'}),
        }



