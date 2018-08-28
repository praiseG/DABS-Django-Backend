from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from dabs.utils import Utils

from .models import MyUser


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'designation',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Utils.get_or_none(MyUser, email=email)
        if qs is not None:
            raise forms.ValidationError("Email already registered")
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.split()) < 2:
            raise forms.ValidationError("Name should include first and Last Name")
        return name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # save password in hash form
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'designation', 'role', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial['password']