from django import forms
from .models import *
from django.forms.widgets import DateInput, TextInput
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models import Sum


class AddChalanForm(forms.ModelForm):
    class Meta:
        model = Chalan
        exclude = ('owner',)
        widgets = {
            'product': TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'SElect Product',
                }
            ),
            'quantity': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            # 'unit': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            'imported_from': TextInput(attrs={'class': 'input', 'placeholder': 'USA'}),
            'import_date': DateInput(attrs={'class': 'input', 'placeholder': 'mm/dd/yyyy'}),
        }


class AddSalesForm(forms.ModelForm):
    class Meta:
        model = SellProduct
        exclude = ('seller',)
        widgets = {
            'buyer': TextInput(attrs={'class': 'input', 'placeholder': "Enter Buyer's Trade License No:"}),
            'product': TextInput(attrs={'class': 'input', 'placeholder': 'Select Product', }),
            'quantity': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            'unit': TextInput(attrs={'class': 'input', 'placeholder': '1', }),
            'price': TextInput(attrs={'class': 'input', 'placeholder': '20'}),
            'sell_date': TextInput(attrs={'class': 'input', 'placeholder': 'mm/dd/yyyy'}),
            'created_at': DateInput(attrs={'class': 'input', 'placeholder': 'mm/dd/yyyy'}),
        }
        error_messages = {
            'buyer': {
                'required': 'Username is required',
                'none': "Buyer with this name doesn't exists"
            },
            'trade_license_no': {
                'required': 'Trade License Number is required'
            }
        }

    def clean(self, *args, **kwargs):
        form_data = self.cleaned_data
        print(form_data)
        user = form_data['buyer']

        if User.objects.filter(trade_license_no=user).exists():

            print("returning form")

            return form_data
        else:
            print("user doesn't exists")
            raise forms.ValidationError(
                "User with this trade license doesn't exists")
            return super(AddSalesForm, self).clean(*args, **kwargs)

    def is_valid(self):
        valid = super(AddSalesForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        sell = super(AddSalesForm, self).save(commit=False)
        if commit:
            sell.save()
        return sell

    # def clean(self, *args, **kwargs):
    #     trade_license_no = self.cleaned_data.get("buyer")
    #     if trade_license_no:
    #         self.user = authenticate(trade_license_no=trade_license_no)

    #         if self.user is None:
    #             raise forms.ValidationError("User Does Not Exist.")
    #         if not self.user.is_active:
    #             raise forms.ValidationError("User is not Active.")

    #     return super(AddSalesForm, self).clean(*args, **kwargs)
