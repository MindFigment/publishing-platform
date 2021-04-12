from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie

from blogs.models import Blog
from tags.models import Tag
from common.utils import unique_slugify

from .forms import PostForm, TitleForm, SubTitleFormset, TextFormset, CitationFormset, ImageFormset
from .models import Citation, Image, Post, Section, Title, SubTitle, Text


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post.objects.prefetch_related('sections').all(),
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'posts/post/post-detail.html',
                  {'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post.objects.all(), id=post_id)
    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


@login_required
@ensure_csrf_cookie
def manage_posts(request, blog_slug):
    blog = get_object_or_404(Blog.objects.all(), slug=blog_slug)
    published_posts = blog.posts.filter(status='publish')
    draft_posts = blog.posts.filter(status='draft')
    return render(request,
                  'posts/post/posts-manage.html',
                  {
                      'blog': blog,
                      'published_posts': published_posts,
                      'draft_posts': draft_posts
                  })


SUBTITLE_PREFIX = 'subtitle'
TEXT_PREFIX = 'text'
CITATION_PREFIX = 'citation'
IMAGE_PREFIX = 'image'


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post.objects.all(), slug=slug)
#     if request.method == 'POST':
#         blog_form = NewBlogForm(request.POST, request.FILES, instance=blog)
#         if blog_form.is_valid():
#             updated_blog = blog_form.save()
#             message = f'{updated_blog.title} updated succesfully'
#             messages.add_message(request, messages.SUCCESS, message)
#             return redirect('blogs:manage_blogs')
#     else:
#         blog_form = NewBlogForm(instance=blog)

#     return render(request,
#                   'blogs/blog/blog-edit.html',
#                   {'blog_form': blog_form})

    # blog = get_object_or_404(Blog.objects.all(), pk=blog_id)

    if request.method == 'GET':
        print('\n\n\nGET\n', request.GET, '\n\n\n')
        post_form = PostForm(instance=post)
        title_form = TitleForm()
        print(post_form, title_form)
        subtitle_formset = SubTitleFormset(prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(prefix=CITATION_PREFIX)
        image_formset = ImageFormset(prefix=IMAGE_PREFIX)
    elif request.method == 'POST':
        print('\n\n\nPOST\n', request.POST, request.FILES, '\n\n\n')
        post_form = PostForm(request.POST)
        title_form = TitleForm(request.POST)
        subtitle_formset = SubTitleFormset(
            request.POST or None, prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(request.POST or None, prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(
            request.POST or None, prefix=CITATION_PREFIX)
        image_formset = ImageFormset(
            data=request.POST or None, files=request.FILES or None, prefix=IMAGE_PREFIX
        )
        # print('\npost request files\n', request.FILES)
        # print('\nimage formset\n', image_formset.files)
        # print(title_form)
        # print('Subtitle formset:', subtitle_formset)
        # print(text_formset)
        if post_form.is_valid() and title_form.is_valid() and subtitle_formset.is_valid() and text_formset.is_valid() and image_formset.is_valid() and citation_formset.is_valid():
            # Create post
            post_cd = post_form.cleaned_data
            post_status = post_cd['status']
            post_tags = post_cd['tags']
            print('POST status:', post_status, ', tags:', post_tags)
            new_story = Post(blog=blog, status=post_status)
            sections = []

            #############
            ### TITLE ###
            #############
            title_cd = title_form.cleaned_data
            title = title_cd['title']
            title_order = title_cd['order']
            print('title:', title, title_order)
            title_object = Title(title=title)
            # title_object.save(commit=False)

            # Automatically updates new_post slug field
            new_slug = unique_slugify(new_story, [title])
            print('new slug:', new_slug)
            new_story.slug = new_slug
            # new_story.save()

            # print('new story', Post.objects.get(pk=new_story.id))

            # sections.append(Section(post=new_story,
            #                         content_object=title_object,
            #                         order=title_order))
            sections.append({
                'content_object': title_object,
                'order': title_order
            })

            print('!', sections)

            # Section.objects.create(post=new_story,
            #                        content_object=title_object,
            #                        order=title_order)

            #################
            ### SUBTITLES ###
            #################
            subtitle_objects = []
            for subtitle_form in subtitle_formset:
                subtitle_cd = subtitle_form.cleaned_data
                subtitle = subtitle_cd['subtitle']
                subtitle_order = subtitle_cd['order']
                subtitle_object = SubTitle(subtitle=subtitle)
                # subtitle_object.save()
                # Section.objects.create(post=new_post,
                #                     content_object=subtitle_object)
                subtitle_objects.append(subtitle_object)
                # sections.append(Section(post=new_story,
                #                         content_object=subtitle_object,
                #                         order=subtitle_order))
                sections.append({
                    'content_object': subtitle_object,
                    'order': subtitle_order
                })

            text_objects = []
            for text_form in text_formset:
                text_cd = text_form.cleaned_data
                text = text_cd['text']
                text_order = text_cd['order']
                text_object = Text(text=text)

                text_objects.append(text_object)
                # sections.append(Section(post=new_story,
                #                         content_object=text_object,
                #                         order=text_order))
                sections.append({
                    'content_object': text_object,
                    'order': text_order
                })

            citation_objects = []
            for citation_form in citation_formset:
                citation_cd = citation_form.cleaned_data
                citation = citation_cd['citation']
                citation_order = citation_cd['order']
                citation_object = Citation(citation=citation)

                citation_objects.append(citation_object)
                # sections.append(Section(post=new_story,
                #                         content_object=citation_object,
                #                         order=citation_order))
                sections.append({
                    'content_object': citation_object,
                    'order': citation_order
                })

            image_objects = []
            for image_form in image_formset:
                image_cd = image_form.cleaned_data
                file = image_cd['file']
                file_order = image_cd['order']
                file_object = Image(file=file)

                image_objects.append(file_object)
                # sections.append(Section(post=new_story,
                #                         content_object=file_object,
                #                         order=file_order))
                sections.append({
                    'content_object': file_object,
                    'order': file_order
                })

            print('\nSECTIONS:\n', sections)

            try:
                with transaction.atomic():
                    post_tags = Tag.tags.add(*post_tags)
                    new_story.save()
                    new_story.tags.add(*post_tags)
                    title_object.save()
                    print('saved title!', title_object.id)
                    print('transaction sections', sections)
                    if len(subtitle_objects):
                        print('subtitle sections')
                        SubTitle.objects.bulk_create(subtitle_objects)
                    if len(text_objects):
                        print('text sections')
                        Text.objects.bulk_create(text_objects)
                    if len(citation_objects):
                        print('citation sections')
                        Citation.objects.bulk_create(citation_objects)
                    if len(image_objects):
                        print('image sections')
                        Image.objects.bulk_create(image_objects)
                    if len(sections):
                        def create_section(args_dict):
                            print('new story', new_story)
                            print('args', args_dict)
                            return Section(post=new_story, **args_dict)
                        print('section sections')
                        sections = map(create_section, sections)
                        print('sections after map', sections)
                        Section.objects.bulk_create(sections)
                    print('END')
            except IntegrityError as e:
                print('Integrity error!', e)
                # Post.objects.get(pk=new_story.id).delete()
                return render(request,
                              'posts/post/write-story.html',
                              {'blog': blog,
                               'post_form': post_form,
                               'title_form': title_form,
                               'subtitle_formset': subtitle_formset,
                               'text_formset': text_formset,
                               'citation_formset': citation_formset,
                               'image_formset': image_formset})

            return redirect(reverse('posts:manage_posts'))

        print('Ups, something went wrong!\n', image_formset)

    print('\nrendering\n')
    return render(request,
                  'posts/post/write-story.html',
                  {'blog': post.blog,
                   'post_form': post_form,
                   'title_form': title_form,
                   'subtitle_formset': subtitle_formset,
                   'text_formset': text_formset,
                   'citation_formset': citation_formset,
                   'image_formset': image_formset})


def create_post(request, blog_id):
    blog = get_object_or_404(Blog.objects.all(), pk=blog_id)

    if request.method == 'GET':
        print('\n\n\nGET\n', request.GET, '\n\n\n')
        post_form = PostForm()
        title_form = TitleForm()
        print(post_form, title_form)
        subtitle_formset = SubTitleFormset(prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(prefix=CITATION_PREFIX)
        image_formset = ImageFormset(prefix=IMAGE_PREFIX)
    elif request.method == 'POST':
        print('\n\n\nPOST\n', request.POST, request.FILES, '\n\n\n')
        post_form = PostForm(request.POST)
        title_form = TitleForm(request.POST)
        subtitle_formset = SubTitleFormset(
            request.POST or None, prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(request.POST or None, prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(
            request.POST or None, prefix=CITATION_PREFIX)
        image_formset = ImageFormset(
            data=request.POST or None, files=request.FILES or None, prefix=IMAGE_PREFIX
        )
        # print('\npost request files\n', request.FILES)
        # print('\nimage formset\n', image_formset.files)
        # print(title_form)
        # print('Subtitle formset:', subtitle_formset)
        # print(text_formset)
        if post_form.is_valid() and title_form.is_valid() and subtitle_formset.is_valid() and text_formset.is_valid() and image_formset.is_valid() and citation_formset.is_valid():
            # Create post
            post_cd = post_form.cleaned_data
            post_status = post_cd['status']
            post_tags = post_cd['tags']
            print('POST status:', post_status, ', tags:', post_tags)
            new_story = Post(blog=blog, status=post_status)
            sections = []

            #############
            ### TITLE ###
            #############
            title_cd = title_form.cleaned_data
            title = title_cd['title']
            title_order = title_cd['order']
            print('title:', title, title_order)
            title_object = Title(title=title)
            # title_object.save(commit=False)

            # Automatically updates new_post slug field
            new_slug = unique_slugify(new_story, [title])
            print('new slug:', new_slug)
            new_story.slug = new_slug
            # new_story.save()

            # print('new story', Post.objects.get(pk=new_story.id))

            # sections.append(Section(post=new_story,
            #                         content_object=title_object,
            #                         order=title_order))
            sections.append({
                'content_object': title_object,
                'order': title_order
            })

            print('!', sections)

            # Section.objects.create(post=new_story,
            #                        content_object=title_object,
            #                        order=title_order)

            #################
            ### SUBTITLES ###
            #################
            subtitle_objects = []
            for subtitle_form in subtitle_formset:
                subtitle_cd = subtitle_form.cleaned_data
                subtitle = subtitle_cd['subtitle']
                subtitle_order = subtitle_cd['order']
                subtitle_object = SubTitle(subtitle=subtitle)
                # subtitle_object.save()
                # Section.objects.create(post=new_post,
                #                     content_object=subtitle_object)
                subtitle_objects.append(subtitle_object)
                # sections.append(Section(post=new_story,
                #                         content_object=subtitle_object,
                #                         order=subtitle_order))
                sections.append({
                    'content_object': subtitle_object,
                    'order': subtitle_order
                })

            text_objects = []
            for text_form in text_formset:
                text_cd = text_form.cleaned_data
                text = text_cd['text']
                text_order = text_cd['order']
                text_object = Text(text=text)

                text_objects.append(text_object)
                # sections.append(Section(post=new_story,
                #                         content_object=text_object,
                #                         order=text_order))
                sections.append({
                    'content_object': text_object,
                    'order': text_order
                })

            citation_objects = []
            for citation_form in citation_formset:
                citation_cd = citation_form.cleaned_data
                citation = citation_cd['citation']
                citation_order = citation_cd['order']
                citation_object = Citation(citation=citation)

                citation_objects.append(citation_object)
                # sections.append(Section(post=new_story,
                #                         content_object=citation_object,
                #                         order=citation_order))
                sections.append({
                    'content_object': citation_object,
                    'order': citation_order
                })

            image_objects = []
            for image_form in image_formset:
                image_cd = image_form.cleaned_data
                file = image_cd['file']
                file_order = image_cd['order']
                file_object = Image(file=file)

                image_objects.append(file_object)
                # sections.append(Section(post=new_story,
                #                         content_object=file_object,
                #                         order=file_order))
                sections.append({
                    'content_object': file_object,
                    'order': file_order
                })

            print('\nSECTIONS:\n', sections)

            try:
                with transaction.atomic():
                    post_tags = Tag.tags.add(*post_tags)
                    new_story.save()
                    new_story.tags.add(*post_tags)
                    title_object.save()
                    print('saved title!', title_object.id)
                    print('transaction sections', sections)
                    if len(subtitle_objects):
                        print('subtitle sections')
                        SubTitle.objects.bulk_create(subtitle_objects)
                    if len(text_objects):
                        print('text sections')
                        Text.objects.bulk_create(text_objects)
                    if len(citation_objects):
                        print('citation sections')
                        Citation.objects.bulk_create(citation_objects)
                    if len(image_objects):
                        print('image sections')
                        Image.objects.bulk_create(image_objects)
                    if len(sections):
                        def create_section(args_dict):
                            print('new story', new_story)
                            print('args', args_dict)
                            return Section(post=new_story, **args_dict)
                        print('section sections')
                        sections = map(create_section, sections)
                        print('sections after map', sections)
                        Section.objects.bulk_create(sections)
                    print('END')
            except IntegrityError as e:
                print('Integrity error!', e)
                # Post.objects.get(pk=new_story.id).delete()
                return render(request,
                              'posts/post/write-story.html',
                              {'blog': blog,
                               'post_form': post_form,
                               'title_form': title_form,
                               'subtitle_formset': subtitle_formset,
                               'text_formset': text_formset,
                               'citation_formset': citation_formset,
                               'image_formset': image_formset})

            return redirect(reverse('blogs:manage_blogs'))

        print('Ups, something went wrong!\n', image_formset)

    print('\nrendering\n')
    return render(request,
                  'posts/post/write-story.html',
                  {'blog': blog,
                   'post_form': post_form,
                   'title_form': title_form,
                   'subtitle_formset': subtitle_formset,
                   'text_formset': text_formset,
                   'citation_formset': citation_formset,
                   'image_formset': image_formset})
