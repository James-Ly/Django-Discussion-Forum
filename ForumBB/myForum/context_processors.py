from myForum import models
from django.http import HttpResponse
from django.template import RequestContext, Template


def number_of_posts(request):
    return {
        'number_of_posts':models.Posts.objects.count()
    }

def number_of_users(request):
    return {
        'number_of_users':models.UserProfile.objects.count()
    }

def number_of_comments(request):
    return {
        'number_of_comments':models.Comments.objects.count()
    }
