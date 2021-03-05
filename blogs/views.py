from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Blog, Post, FollowRelationship
from .forms import NewBlogForm
from common.utils import unique_slugify
from common.decorators import ajax_required
# from comments.models import Comment
# from comments.forms import CommentForm


def blog_list(request):
    blogs = Blog.active.all()
    return render(request, 'blogs/blog/list.html', {'blogs': blogs})


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    posts = blog.posts.filter(status='published')
    return render(request, 'blogs/blog/detail.html',
                  {'blog': blog,
                   'posts': posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status='published',
                             publish__year=year, publish__month=month, publish__day=day)

    # comments = post.comments.filter(active=True)
    # new_comment = None

    # if request.method == 'POST':
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.post = post
    #         new_comment.save()
    # else:
    #     comment_form = CommentForm()

    return render(request,
                  'blogs/post/detail.html',
                  {'post': post})


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
    return render(request,
                  'blogs/blog/new_blog.html',
                  {'blog_form': blog_form})


@login_required
def manage_blogs(request):
    user_id = request.user.id
    user_blogs = Blog.objects.filter(author__id=user_id)
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
