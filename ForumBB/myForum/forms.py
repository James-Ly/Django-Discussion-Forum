from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Comments, Posts
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta():
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Please enter your username here',
                       'autocomplete': 'off'}),
        }

    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        password_conf = all_clean_data['password_confirmation']
        if password != password_conf:
            raise forms.ValidationError('Password and Password Confirmation must match')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('profile_pic', 'forum_email')
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'forum_email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Please enter your email here', 'autocomplete': 'off'}),
        }

    def clean(self):
        all_clean_data = super().clean()


class PostForm(forms.ModelForm):
    class Meta():
        model = Posts
        fields = ['title', ]


class CommentsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget)

    class Meta():
        model = Comments
        fields = ['content', ]


class CommentsAdmin(admin.ModelAdmin):
    form = CommentsForm
