from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        print("Sending form", form)
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/registration/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def profile_detail(request, username):
    profile = Profile.objects.select_related('user').get(user__username=username,
                                                         user__is_active=True)
    print(profile)
    return render(request,
                  'account/profile/detail.html',
                  {'profile': profile})


@require_GET
@login_required
def user_followers(request):
    profile = request.user.profile
    old_followers, new_followers = profile.get_old_and_new_followers()

    old_paginator = Paginator(old_followers, 5)
    new_paginator = Paginator(new_followers, 5)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        page = request.GET.get('page')
        new_or_old = request.GET.get('which')
        try:
            if new_or_old == 'NEW':
                followers = new_paginator.page(page)
                profile.set_followers_as_old(followers)
            else:
                followers = old_paginator.page(page)
        except InvalidPage:
            return HttpResponse('')
        return render(request,
                      'account/profile/followers_ajax_list.html',
                      {
                          'blog': False,
                          'followers': followers
                      })
    else:
        try:
            old_followers = old_paginator.page(1)
        except EmptyPage:
            old_followers = []
        try:
            new_followers = new_paginator.page(1)
            profile.set_followers_as_old(new_followers)
        except EmptyPage:
            new_followers = []

    return render(request,
                  'account/profile/followers_list.html',
                  {
                      'blog': False,
                      'new_followers': new_followers,
                      'old_followers': old_followers,
                  })
