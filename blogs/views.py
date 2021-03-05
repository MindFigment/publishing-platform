from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Blog, Post
from .forms import NewBlogForm
from common.utils.slug import unique_slugify
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
    if request.method == 'POST':
        blog_form = NewBlogForm(data=request.POST,
                                files=request.FILES)
        if blog_form.is_valid():
            # Create a new blog object but avoid saving it yet
            new_blog = blog_form.save(commit=False)
            new_slug = unique_slugify(new_blog, [new_blog.title])
            print('new_slug', new_slug, new_blog.slug)
            new_blog.author = request.user
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
