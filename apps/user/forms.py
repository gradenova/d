from django import forms

class LoginForm(forms.Form):

    identity = forms.CharField(required=True)

    password = forms.CharField(required=True, widget=forms.PasswordInput)

    username = forms.CharField(required=True)   #教师登录时使用教职工号登录



