from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Enter a valid email address")

    class Meta:
        model = Account
        fields = ('email', 'name', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(
            'Email "%s" is already in use.' % email)


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' % username)

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Inavalid Login Details")


class AccountUpdateForm(forms.ModelForm):
    account_type = forms.BooleanField(required=False)

    class Meta:
        model = Account
        fields = ('name', 'email', 'username', 'bio', 'profile_picture', 'account_type')


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(
            'Username "%s" is already in use.' % username)

    def clean_account_type(self):
        account_type = self.cleaned_data['account_type']
        if account_type == True:
            account= Account.objects.filter(username=self.instance).update(account_type='private')
            account_type = 'private'
            return account_type
        elif account_type == False:
            account= Account.objects.filter(username=self.instance).update(account_type='public')
            account_type = 'public'
            return account_type


    def save(self, commit=True):
        account = self.instance
        account.email = self.cleaned_data['email']
        account.username = self.cleaned_data['username']
        if self.cleaned_data['username']:
            account.slug = self.cleaned_data['username']

        if self.cleaned_data['profile_picture']:
            account.profile_picture = self.cleaned_data['profile_picture']
            
        if commit:
            account.save()
        return account
