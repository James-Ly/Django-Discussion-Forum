from django.urls import path
from . import views

app_name = 'myForum'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('register/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('post_list/<subsection>/', views.posts_list.as_view(), name='posts_list'),
    path('comment_list/<subsection>/<post>/', views.comments_list.as_view(), name='comments_list'),
    path('create_comment/<subsection>/<post>/', views.CreateComment.as_view(), name='create_comment'),
    path('user_profile/<int:pk>/', views.User_Profile.as_view(), name='user_profile'),
]
