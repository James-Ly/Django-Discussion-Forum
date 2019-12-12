from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class UserProfile(models.Model):
    '''
    Model for the User profile
    contains the username, email, password, login, last_login and date_joined
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    '''
    Additional attribute for the user
    1: Profile pic
    2: Title: Will add later
    '''
    forum_email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return "@{}".format(self.user.username)


class Section(models.Model):
    title = models.CharField(max_length=265, blank=False, null=False, )
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class SubSection(models.Model):
    title = models.CharField(max_length=355, blank=False, null=False)
    description = models.CharField(max_length=500)
    section = models.ForeignKey(Section, related_name='section', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.title

    def latestpost(self):
        return self.subsection.order_by('-created_date')


class Posts(models.Model):
    title = models.CharField(max_length=355)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    subsection = models.ForeignKey(SubSection, related_name='subsection', on_delete=models.CASCADE, blank=False,
                                   null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        pass