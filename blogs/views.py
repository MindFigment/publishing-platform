from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import InvalidPage, Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json

from tags.models import Tag
from common.utils import unique_slugify

from .models import Blog, FollowRelationship
from .forms import NewBlogForm


def blog_list(request):
    blogs = Blog.active.all()
    return render(request, 'blogs/blog/list.html', {'blogs': blogs})


def blog_ajax_list(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 8)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # if page is not a integer deliver the first page
        blogs = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        blogs = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'blogs/blog/blogs_ajax_list.html',
                      {'blogs': blogs})
    return render(request,
                  'blogs/blog/list.html',
                  {'blogs': blogs})


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    posts = blog.posts.all().prefetch_related('sections')
    return render(request, 'blogs/blog/detail.html',
                  {'blog': blog,
                   'posts': posts})


@login_required
def new_blog(request):
    print('New blog', request)
    if request.method == 'POST':
        blog_form = NewBlogForm(data=request.POST,
                                files=request.FILES)
        if blog_form.is_valid():
            new_blog = blog_form.save(author=request.user.profile)
            return render(request,
                          'blogs/blog/detail.html',
                          {'blog': new_blog})
    else:
        blog_form = NewBlogForm()
        print(blog_form)
    return render(request,
                  'blogs/blog/new_blog.html',
                  {'blog_form': blog_form})


@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog.objects.all(), slug=slug)
    if request.method == 'POST':
        blog_form = NewBlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            updated_blog = blog_form.save()
            message = f'{updated_blog.title} updated succesfully'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('blogs:manage_blogs')
    else:
        blog_form = NewBlogForm(instance=blog)

    return render(request,
                  'blogs/blog/edit_blog.html',
                  {'blog_form': blog_form})


@login_required
# @csrf_exempt
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog.objects.all(), id=blog_id)
    if request.method == 'DELETE':
        blog.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


@login_required
@ensure_csrf_cookie
def manage_blogs(request):
    user_id = request.user.id
    user_blogs = Blog.objects.filter(author__user__id=user_id)
    active_blogs = user_blogs.filter(is_active=True)
    inactive_blogs = user_blogs.filter(is_active=False)
    return render(request,
                  'blogs/blog/manage_blogs.html',
                  {'active_blogs': active_blogs,
                   'inactive_blogs': inactive_blogs})


@require_POST
@login_required
def blog_follow(request):
    post_data = json.loads(request.body.decode('utf-8'))
    blog_id = post_data.get('id')
    action = post_data.get('action')
    print(blog_id, action)
    if blog_id and action:
        try:
            blog = Blog.objects.get(id=blog_id)
            if action == 'follow':
                FollowRelationship.objects.create(
                    blog=blog,
                    profile=request.user.profile
                )
            else:
                FollowRelationship.objects.filter(
                    blog=blog,
                    profile=request.user.profile
                ).delete()
            return JsonResponse({'status': 'ok'})
        except Blog.DoesNotExist:
            return JsonResponse({'status': 'error'})
    print(':(')
    return JsonResponse({'status': 'error'})


@require_GET
@login_required
def blog_followers(request, slug):
    blog = get_object_or_404(Blog.objects.all(), slug=slug)
    old_followers = blog.get_old_followers()
    new_followers = blog.get_new_followers()

    old_paginator = Paginator(old_followers, 5)
    new_paginator = Paginator(new_followers, 5)

    print('old', old_followers)
    print('new', new_followers)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        page = request.GET.get('page')
        new_or_old = request.GET.get('which')
        print('page', page, new_or_old)
        try:
            if new_or_old == 'NEW':
                followers = new_paginator.page(page)
            else:
                followers = old_paginator.page(page)
        except InvalidPage:
            return HttpResponse('')
        return render(request,
                      'account/profile/followers_ajax_list.html',
                      {
                          'blog': blog,
                          'followers': followers
                      })
    else:
        try:
            new_followers = new_paginator.page(1)
        except EmptyPage:
            new_followers = []
        try:
            old_followers = old_paginator.page(1)
        except EmptyPage:
            old_followers = []

    return render(request,
                  'account/profile/followers_list.html',
                  {
                      'blog': blog,
                      'new_followers': new_followers,
                      'old_followers': old_followers,
                  })
