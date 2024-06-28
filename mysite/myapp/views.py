from django.shortcuts import render, redirect, get_object_or_404
from . import forms, views
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm, CreatePostForm
from .models import Posts
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.contrib.messages import constants as message_constants
from django.http import Http404

class HomeView(TemplateView):
    template_name = 'home.html'
    
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    
class UserLoginView(FormView):
    template_name = 'user_login.html'
    form_class = UserLoginForm
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            if user is not None and user.is_active:
                login(request, user)
                return redirect('myapp:user')
            else:
                messages.add_message(request, message_constants.ERROR, 'アカウントが存在しません。')
        else:
            messages.add_message(request, message_constants.ERROR, 'メールアドレスかパスワードが違います。')
            return redirect('myapp:user')

class UserLogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'ログアウトしました。')
        return redirect('myapp:user_login')

@login_required
def user_edit(request):
    user_edit_form = forms.UserEditForm(request.POST or None, instance=request.user)
    if user_edit_form.is_valid():
        messages.success(request, '更新完了しました。')
        user_edit_form.save()
    return render(request, 'user_edit.html', context={
        'user_edit_form': user_edit_form,
    })

@login_required
def change_password(request):
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワード更新完了しました。')
            update_session_auth_hash(request, request.user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(
        request, 'change_password.html', context={
            'password_change_form': password_change_form,
        }
    )

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = CreatePostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('myapp:create_post.html')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '記事を投稿しました。')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('myapp:list_posts.html')

class PostListView(ListView):
    model = Posts
    template_name = 'list_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Posts.objects.fetch_all_posts()
 
 
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = CreatePostForm
    template_name = 'myapp/edit_post.html'
    context_object_name = 'edit_post_form'

    def get_object(self, queryset=None):
        post = get_object_or_404(Posts, id=self.kwargs['id'])
        if post.user.id != self.request.user.id:
            raise Http404
        return post

    def form_valid(self, form):
        messages.success(self.request, '投稿を更新しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('myapp:list_posts.html')
