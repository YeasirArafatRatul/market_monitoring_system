from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import TextInput, EmailInput, Select, FileInput
from accounts.models import User, UserProfile
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy


ROLE = (
    ('retailer', 'Retailer'),
    ('importer', 'Importer'),
    ('wholeseller', 'Whole Seller'),
)


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    trade_license_no = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Trade License No",
                "class": "form-control"
            }
        )
    )

    role = forms.ChoiceField(
        choices=ROLE,
        widget=forms.Select(
            attrs={
                "placeholder": "Who are you?",
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ['username', 'email', 'trade_license_no', 'role',
                  'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Username is required',
                'max_length': 'Username is too long'
            },
            'email': {
                'required': 'Email is required',
            },
            'trade_license_no': {
                'required': 'Trade License Number is required'
            }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': TextInput(
                attrs={
                    "placeholder": "Username",
                    "class": "form-control",
                    'disabled': 'true'
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'email'
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ('image', 'division', 'district', 'upazila',
                  'industry_type',)

        widgets = {
            'image': FileInput(
                attrs={
                    "placeholder": "Profile Photo",
                    "class": "form-control",
                }
            ),
            'division': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Division'
                }
            ),
            'district': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'District'
                }
            ),
            'upazila': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Upzilla'
                }
            ),
            'industry_type': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Industry Type'
                }
            ),

        }
        # widgets = {
        #     'image': FileInput(attrs={'class': 'input', 'placeholder': 'profile picture', }),
        #     'cover_img': FileInput(attrs={'class': 'input', 'placeholder': 'cover photo', }),
        #     'about': TextInput(attrs={'class': 'input', 'placeholder': 'Say Something About You...'}),
        #     'address': TextInput(attrs={'class': 'input', 'placeholder': 'Enter Address'}),
        #     'website': TextInput(attrs={'class': 'input', 'placeholder': 'https://www.example.com'})
        # }
