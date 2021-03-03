from django.shortcuts import get_object_or_404, render
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Blog, Post
from comments.models import Comment
from comments.forms import CommentForm


def blog_list(request):
    blogs = Blog.active.all()
    return render(request, 'blogs/blog/list.html', {'blogs': blogs})


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    posts = blog.posts.filter(status='published')
    print(blog)
    print(posts)
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
