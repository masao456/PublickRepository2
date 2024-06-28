from django.urls import path
from django.contrib import admin
from .views import RegistUserView, HomeView, UserLoginView, UserLogoutView, UserView, CreatePostView, PostListView, EditPostView
from . import views

app_name = 'myapp'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('user/', UserView.as_view(), name='user'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('list_posts/', PostListView.as_view(), name='list_posts'),
    path('edit_post<int:id>/', EditPostView.as_view(), name='edit_post'),
]