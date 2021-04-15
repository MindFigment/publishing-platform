import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from common.encoders import ExtendedEncoder
from posts.models import Post

from .forms import (LoginForm, ProfileEditForm, UserEditForm,
                    UserRegistrationForm)
from .models import Profile


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def dashboard(request):

    profile = request.user.profile
    blog_results = profile.following.exclude(author=profile.pk).order_by("-created")
    post_results = Post.published.filter(blog__in=blog_results).order_by("-publish")

    post_results = [json.dumps(p, cls=ExtendedEncoder) for p in post_results]

    blog_results = [json.dumps(b, cls=ExtendedEncoder) for b in blog_results]

    return render(
        request,
        "account/dashboard.html",
        {
            "post_results": post_results,
            "blog_results": blog_results,
        },
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request,
                "account/registration/register_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request, "account/registration/register.html", {"user_form": user_form}
    )


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(
                request,
                "account/profile/detail.html",
                {"profile": request.user.profile},
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def profile_detail(request, username):
    profile = Profile.objects.select_related("user").get(
        user__username=username, user__is_active=True
    )
    return render(request, "account/profile/detail.html", {"profile": profile})


@require_GET
@login_required
def user_followers(request):
    profile = request.user.profile
    old_followers, new_followers = profile.get_old_and_new_followers()
    all_followers = new_followers | old_followers
    paginator = Paginator(all_followers, 20)

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        page = request.GET.get("page")
        try:
            followers = list(paginator.page(page))
        except InvalidPage:
            return HttpResponse("")

        profile.set_followers_as_old(new_followers)

        return render(
            request,
            "account/profile/followers-ajax-list.html",
            {"blog": False, "followers": followers},
        )
    else:
        try:
            followers = list(paginator.page(1))
        except EmptyPage:
            followers = []

    profile.set_followers_as_old(new_followers)

    return render(
        request,
        "account/profile/followers-list.html",
        {
            "blog": False,
            "followers": followers,
        },
    )
