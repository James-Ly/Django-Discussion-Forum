from django.urls import path
from . import views

app_name = 'myForum'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('register/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('subsection_list/<section>/', views.subsection_list.as_view(), name='subsection_list'),
    path('post_list/<section>/<subsection>/', views.posts_list.as_view(), name='posts_list'),
    path('comment_list/<subsection>/<post>/', views.comments_list.as_view(), name='comments_list'),
    path('commentcreate/<subsection>/<post>/', views.CommentCreate, name='commentcreate'),
    path('createcomment/<subsection>/<post>', views.CreateComment, name='createcomment'),
    path('user_profile/<int:pk>/', views.User_Profile.as_view(), name='user_profile'),

]
