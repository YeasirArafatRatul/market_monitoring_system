from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import TextInput, EmailInput, Select, FileInput
from accounts.models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['email'].label = "Email"
        self.fields['trade_license_no'].label = "Trade License No"
        self.fields['role'].label = "Who Are You?"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Username',
            }
        )

        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['trade_license_no'].widget.attrs.update(
            {
                'placeholder': 'Enter Trade License',
            }
        )
        self.fields['role'].widget.attrs.update(
            {
                'placeholder': 'Who Are You?',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )

        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'trade_license_no','role',
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
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Enter Password'})

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
            'username': TextInput(attrs={'class': 'input', 'placeholder': ' Username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),

        }

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']
       

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        fields = ('image','division', 'district', 'upazila',
                  'industry_type',)
        # widgets = {
        #     'image': FileInput(attrs={'class': 'input', 'placeholder': 'profile picture', }),
        #     'cover_img': FileInput(attrs={'class': 'input', 'placeholder': 'cover photo', }),
        #     'about': TextInput(attrs={'class': 'input', 'placeholder': 'Say Something About You...'}),
        #     'address': TextInput(attrs={'class': 'input', 'placeholder': 'Enter Address'}),
        #     'website': TextInput(attrs={'class': 'input', 'placeholder': 'https://www.example.com'})
        # }

