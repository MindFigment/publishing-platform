from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Blog, FollowRelationship
from .forms import NewBlogForm
from common.utils import unique_slugify
from common.decorators import ajax_required
# from comments.models import Comment
# from comments.forms import CommentForm


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
                      'blogs/blog/ajax_list.html',
                      {'blogs': blogs})
    return render(request,
                  'blogs/blog/list.html',
                  {'blogs': blogs})


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    # posts = blog.posts.filter(status='published')
    posts = blog.posts.all()
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
            # Create a new blog object but avoid saving it yet
            new_blog = blog_form.save(commit=False)
            new_slug = unique_slugify(new_blog, [new_blog.title])
            print('new_slug', new_slug, new_blog.slug)
            new_blog.author = request.user.profile
            # Save the Blog object
            new_blog.save()
            return render(request,
                          'blogs/blog/detail.html',
                          {'blog': new_blog})
    else:
        blog_form = NewBlogForm()
        print(blog_form)
    return render(request,
                  'blogs/blog/new_blog.html',
                  {'blog_form': blog_form})


#######
#######
#######

def hand_crafted_redirect_response(request):
    response = HttpResponse(status=302)
    response['Location'] = 'url...'
    # return HttpResponseRedirect(url...)
    return response


def model_redirect_view(request):
    blog = Blog.objects.first()
    # Will call blog.get_absolute_url() to set redirect target url
    http_response_redirect = redirect(blog)
    print(http_response_redirect.url)
    return http_response_redirect


def fixed_featured_product_view(request):
    blog = Blog.objects.first()


#######
#######
#######


@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        print('request')
        print(request.POST)
        print(request.FILES)
        print(blog)
        blog_form = NewBlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            updated_blog = blog_form.save(commit=False)
            updated_slug = unique_slugify(updated_blog, [updated_blog.title])
            print('updated slug', updated_slug)
            updated_blog.save()
            message = f'{updated_blog.title} updated succesfully'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('blogs:manage_blogs')
    else:
        blog_form = NewBlogForm(instance=blog)
    return render(request,
                  'blogs/blog/edit_blog.html',
                  {'blog_form': blog_form})


@login_required
def manage_blogs(request):
    user_id = request.user.id
    user_blogs = Blog.objects.filter(author__user__id=user_id)
    active_blogs = user_blogs.filter(is_active=True)
    inactive_blogs = user_blogs.filter(is_active=False)
    return render(request,
                  'blogs/blog/manage_blogs.html',
                  {'active_blogs': active_blogs,
                   'inactive_blogs': inactive_blogs})


@ajax_required
@require_POST
@login_required
def blog_follow(request):
    blog_id = request.POST.get('id')
    action = request.POST.get('action')
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
    return JsonResponse({'status': 'error'})
