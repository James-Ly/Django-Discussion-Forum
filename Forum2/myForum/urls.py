from django.urls import path
from . import views

app_name = 'myForum'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('register/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('post_list/<subsection>', views.posts_list.as_view(), name='posts_list'),
]
