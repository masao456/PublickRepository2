from django import forms
from .models import Users, Posts, Comments
from django.contrib.auth.password_validation import validate_password


class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    
    class Meta:
        model = Users
        fields = ['username', 'email', 'password']
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    
class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')

    class Meta:
        model = Users
        fields = ['username', 'email']
        
class PasswordChangeForm(forms.ModelForm):

    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = Users
        fields = ['password', ]
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    
class CreatePostForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    content = forms.CharField(label='コンテンツ', widget=forms.Textarea)
    image = forms.ImageField(label='写真')
    
    class Meta:
        model = Posts
        fields = ['title', 'content', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        
class EditPostForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    content = forms.CharField(label='コンテンツ', widget=forms.Textarea)
    image = forms.ImageField(label='写真')
    class Meta:
        model = Posts
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['content'].required = False
        self.fields['image'].required = False
        
class DeletePostForm(forms.ModelForm):
    confirm_delete = forms.BooleanField(label='削除を確認する', required=True)
    
    class Meta:
        model = Posts
        fields = []
        
class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    
    class Meta:
        model = Comments
        fields = ('comment',)