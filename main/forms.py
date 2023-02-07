from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Talk, User

class SignUpForm(UserCreationForm):
    class Meta:
        #UserCreationForm と AbstractUserは別物であり、
        # model = User の 1 行によって、入力情報が保存される場合の
        # 保存先が User モデルであるという紐づけが行われている
        model = User
        fields = ("username", "email")

class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("message",)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}
        help_texts = {"username": ""}

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}

