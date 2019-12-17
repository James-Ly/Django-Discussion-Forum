from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from myForum import forms
from myForum import models

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.template import RequestContext

# Import the decorators and class Extension to check login session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class HomePage(generic.ListView):
    model = models.Section


def register(request):
    '''
    Register view that allow user to create a new account
    1. If the user has already logged in, the view will redirect him/ or her to the main page
    2. Otherwise, a new account will be create and user will be redirect to the login page
    '''
    if request.user.is_authenticated:
        return redirect('myForum:homepage')
    else:
        registered = False
        if request.method == 'POST':
            user_form = forms.UserForm(data=request.POST)
            profile_form = forms.UserProfileInfoForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                # Hashing password
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile.save()
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            user_form = forms.UserForm()
            profile_form = forms.UserProfileInfoForm()

        if registered:
            return redirect('myForum:login')

        return render(request, 'myForum/register.html',
                      context={'user_form': user_form,
                               'profile_form': profile_form,
                               'registered': registered})


@login_required
def user_logout(request):
    '''
    Logout view
    '''
    logout(request)
    return HttpResponseRedirect(reverse('myForum:homepage'))


class User_Profile(generic.DetailView):
    template_name = 'myForum/user_profile.html'
    model = models.UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.kwargs.get('user_profile')
        return context


def user_login(request):
    '''
    View for user to login into the website
    1. If the user has already logged in, the view will redirect him/ or her to the home page
    2. Else it will check whether the username and the password that user has entered is valid and respond correspondingly
    '''
    if request.user.is_authenticated:
        return redirect('myForum:homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('myForum:homepage')
                else:
                    return HttpResponse('Account not active')
            else:
                print('Someone tried to login and failed')
                print('Username: {} and password {}'.format(username, password))
                return HttpResponse("Invalid login details supplied")
        else:
            return render(request, 'myForum/login.html')


'''
VIEW FOR SUB-SECTION
'''


class subsection_list(generic.ListView):
    model = models.SubSection
    template_name = 'myForum/subsection_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.kwargs.get('section')
        return context


class posts_list(generic.ListView):
    model = models.Posts
    paginate_by = 25

    '''
    Get_queryset function will return a list of the posts which are related to the subsection's title 
    '''

    def get_queryset(self):
        try:
            self.posts_list = models.Posts.objects.filter(
                subsection__title__iexact=self.kwargs.get('subsection')).order_by('-created_date')
        except models.Posts.DoesNotExist:
            raise Http404
        return self.posts_list.all()

    '''
    Beside the posts, the listview will also return the name of the subsection
    '''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subsection'] = self.kwargs.get('subsection')
        context['section'] = self.kwargs.get('section')
        return context


@login_required
def create_post(request, subsection):
    '''
    Create new post and comment
    '''
    if request.method == 'POST':
        post_form = forms.PostForm(data=request.POST)
        comment_form = forms.CommentsForm(data=request.POST)
        if post_form.is_valid() and comment_form.is_valid():
            newpost = post_form.save(commit=False)
            newpost.subsection = models.SubSection.objects.get(title__iexact=subsection)
            newpost.user = request.user.userprofile
            newpost.save()
            newcomment = comment_form.save(commit=False)
            newcomment.post = newpost
            newcomment.user = request.user.userprofile
            newcomment.save()
            return HttpResponseRedirect(reverse('myForum:comments_list',
                                                kwargs={'post': newpost.title, 'subsection': newpost.subsection.title}))
        else:
            print(post_form.errors, comment_form.errors)
    post_form = forms.PostForm()
    comment_form = forms.CommentsForm()
    return render(request, 'myForum/createpost.html',
                  {'post_form': post_form, 'comment_form': comment_form, 'subsection': subsection,
                   'section': models.SubSection.objects.get(title__iexact=subsection).section.title})


class comments_list(generic.ListView):
    '''
    List view for the comments
    '''
    model = models.Comments
    paginate_by = 10

    def get_queryset(self):
        '''
        The object_list returned will be order by created_date
        '''
        try:
            self.comments = models.Comments.objects.filter(post__title__iexact=self.kwargs.get('post')).order_by(
                'created_date')
        except models.Comments.DoesNotExist:
            raise Http404
        return self.comments.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        The other parameters passed to the template include the post title and the subsection title for bread crumb
        '''
        context = super().get_context_data(**kwargs)
        context['post'] = self.kwargs.get('post')
        context['subsection'] = self.kwargs.get('subsection')
        section = models.SubSection.objects.get(title__iexact=self.kwargs.get('subsection')).section
        context['section'] = section.title
        return context


@login_required


def CommentCreate(request, subsection, post):
    form = forms.CommentsForm()
    post = post
    subsection = subsection
    section = models.SubSection.objects.get(title__iexact=subsection).section.title
    return render(request, 'myForum/commentcreate.html',
                  {'form': form, 'post': post, 'subsection': subsection, 'section': section})


@login_required
def CreateComment(request, post, subsection):
    if request.method == 'POST':
        comment_form = forms.CommentsForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user.userprofile
            comment.post = models.Posts.objects.get(title__iexact=post)
            comment.save()
        else:
            print(comment_form.errors)
    return HttpResponseRedirect(reverse('myForum:comments_list', kwargs={'post': post, 'subsection': subsection}))
