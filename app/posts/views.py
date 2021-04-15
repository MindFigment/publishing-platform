from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from blogs.models import Blog
from common.utils import unique_slugify
from tags.models import Tag

from .forms import (CitationFormset, ImageFormset, PostForm, SubTitleFormset,
                    TextFormset, TitleForm)
from .models import Citation, Image, Post, Section, SubTitle, Text, Title


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post.objects.prefetch_related("sections").all(),
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "posts/post/post-detail.html", {"post": post})


def post_list(request):
    return render(request, "posts/post/posts-list.html", {})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post.objects.all(), id=post_id)
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})


@login_required
@ensure_csrf_cookie
def manage_posts(request, blog_slug):
    blog = get_object_or_404(Blog.objects.all(), slug=blog_slug)
    published_posts = blog.posts.filter(status="published")
    draft_posts = blog.posts.filter(status="draft")
    return render(
        request,
        "posts/post/posts-manage.html",
        {"blog": blog, "published_posts": published_posts, "draft_posts": draft_posts},
    )


SUBTITLE_PREFIX = "subtitle"
TEXT_PREFIX = "text"
CITATION_PREFIX = "citation"
IMAGE_PREFIX = "image"


@login_required
def edit_post(request, post_slug):
    post = get_object_or_404(Post.objects.all(), slug=post_slug)
    blog = post.blog

    if request.method == "GET":
        post_form = PostForm(instance=post)
        title_form = TitleForm(data=post.get_title_section())
        subtitle_formset = SubTitleFormset(
            initial=post.get_subtitle_sections(), prefix=SUBTITLE_PREFIX
        )
        text_formset = TextFormset(initial=post.get_text_sections(), prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(
            initial=post.get_citation_sections(), prefix=CITATION_PREFIX
        )
        image_formset = ImageFormset(
            initial=post.get_image_sections(),
            prefix=IMAGE_PREFIX,
        )
    elif request.method == "POST":

        post_form = PostForm(request.POST)
        title_form = TitleForm(request.POST)
        subtitle_formset = SubTitleFormset(request.POST or None, prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(request.POST or None, prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(request.POST or None, prefix=CITATION_PREFIX)
        image_formset = ImageFormset(
            data=request.POST or None, files=request.FILES or None, prefix=IMAGE_PREFIX
        )

        if (
            post_form.is_valid()
            and title_form.is_valid()
            and subtitle_formset.is_valid()
            and text_formset.is_valid()
            and citation_formset.is_valid()
        ):

            post_cd = post_form.cleaned_data
            post_status = post_cd["status"]
            post_tags = post_cd["tags"]
            new_story = post
            new_story.status = post_status
            sections = []

            #########
            # TITLE #
            #########
            title_cd = title_form.cleaned_data
            title = title_cd["title"]
            title_order = title_cd["order"]
            title_object = Title(title=title)

            sections.append({"content_object": title_object, "order": title_order})

            new_slug = unique_slugify(new_story, [title])
            new_story.slug = new_slug

            #############
            # SUBTITLES #
            #############
            subtitle_objects = []
            for subtitle_form in subtitle_formset:
                subtitle_cd = subtitle_form.cleaned_data
                subtitle = subtitle_cd["subtitle"]
                subtitle_order = subtitle_cd["order"]
                subtitle_object = SubTitle(subtitle=subtitle)
                subtitle_objects.append(subtitle_object)
                sections.append(
                    {"content_object": subtitle_object, "order": subtitle_order}
                )

            text_objects = []
            for text_form in text_formset:
                text_cd = text_form.cleaned_data
                text = text_cd["text"]
                text_order = text_cd["order"]
                text_object = Text(text=text)

                text_objects.append(text_object)
                sections.append({"content_object": text_object, "order": text_order})

            citation_objects = []
            for citation_form in citation_formset:
                citation_cd = citation_form.cleaned_data
                citation = citation_cd["citation"]
                citation_order = citation_cd["order"]
                citation_object = Citation(citation=citation)

                citation_objects.append(citation_object)
                sections.append(
                    {"content_object": citation_object, "order": citation_order}
                )

            image_objects = []
            if image_formset.is_valid():
                image_objects = []
                for image_form in image_formset:
                    image_cd = image_form.cleaned_data
                    file = image_cd["file"]
                    file_order = image_cd["order"]
                    file_object = Image(file=file)

                    image_objects.append(file_object)
                    sections.append(
                        {"content_object": file_object, "order": file_order}
                    )

            try:
                with transaction.atomic():
                    post_tags = Tag.tags.add(*post_tags)
                    new_story.save()
                    if post_tags:
                        new_story.tags.set(post_tags)
                    else:
                        new_story.tags.all().delete()
                    title_object.save()
                    if len(subtitle_objects):
                        SubTitle.objects.bulk_create(subtitle_objects)
                    if len(text_objects):
                        Text.objects.bulk_create(text_objects)
                    if len(citation_objects):
                        Citation.objects.bulk_create(citation_objects)
                    if len(image_objects):
                        Image.objects.bulk_create(image_objects)
                    if len(sections):

                        def create_section(args_dict):
                            return Section(post=new_story, **args_dict)

                        if image_objects:
                            new_story.sections.all().delete()
                        else:
                            image_id = ContentType.objects.get_for_model(Image).id
                            new_story.sections.exclude(content_type=image_id).delete()
                        sections = map(create_section, sections)
                        Section.objects.bulk_create(sections)
            except IntegrityError as e:
                print("Integrity error!", e)

                return render(
                    request,
                    "posts/post/edit-story.html",
                    {
                        "blog": blog,
                        "post_form": post_form,
                        "title_form": title_form,
                        "subtitle_formset": subtitle_formset,
                        "text_formset": text_formset,
                        "citation_formset": citation_formset,
                        "image_formset": image_formset,
                    },
                )

            return redirect(reverse("posts:manage_posts", args=[blog.slug]))

    return render(
        request,
        "posts/post/edit-story.html",
        {
            "post": post,
            "blog": blog,
            "post_form": post_form,
            "title_form": title_form,
            "subtitle_formset": subtitle_formset,
            "text_formset": text_formset,
            "citation_formset": citation_formset,
            "image_formset": image_formset,
        },
    )


def create_post(request, blog_id):
    blog = get_object_or_404(Blog.objects.all(), pk=blog_id)

    if request.method == "GET":
        post_form = PostForm()
        title_form = TitleForm()
        subtitle_formset = SubTitleFormset(prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(prefix=CITATION_PREFIX)
        image_formset = ImageFormset(prefix=IMAGE_PREFIX)
    elif request.method == "POST":
        post_form = PostForm(request.POST)
        title_form = TitleForm(request.POST)
        subtitle_formset = SubTitleFormset(request.POST or None, prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(request.POST or None, prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(request.POST or None, prefix=CITATION_PREFIX)
        image_formset = ImageFormset(
            data=request.POST or None, files=request.FILES or None, prefix=IMAGE_PREFIX
        )

        if (
            post_form.is_valid()
            and title_form.is_valid()
            and subtitle_formset.is_valid()
            and text_formset.is_valid()
            and image_formset.is_valid()
            and citation_formset.is_valid()
        ):

            post_cd = post_form.cleaned_data
            post_status = post_cd["status"]
            post_tags = post_cd["tags"]
            new_story = Post(blog=blog, status=post_status)
            sections = []

            #########
            # TITLE #
            #########
            title_cd = title_form.cleaned_data
            title = title_cd["title"]
            title_order = title_cd["order"]
            title_object = Title(title=title)

            # Automatically updates new_post slug field
            new_slug = unique_slugify(new_story, [title])
            new_story.slug = new_slug

            sections.append({"content_object": title_object, "order": title_order})

            #############
            # SUBTITLES #
            #############
            subtitle_objects = []
            for subtitle_form in subtitle_formset:
                subtitle_cd = subtitle_form.cleaned_data
                subtitle = subtitle_cd["subtitle"]
                subtitle_order = subtitle_cd["order"]
                subtitle_object = SubTitle(subtitle=subtitle)
                subtitle_objects.append(subtitle_object)
                sections.append(
                    {"content_object": subtitle_object, "order": subtitle_order}
                )

            text_objects = []
            for text_form in text_formset:
                text_cd = text_form.cleaned_data
                text = text_cd["text"]
                text_order = text_cd["order"]
                text_object = Text(text=text)

                text_objects.append(text_object)
                sections.append({"content_object": text_object, "order": text_order})

            citation_objects = []
            for citation_form in citation_formset:
                citation_cd = citation_form.cleaned_data
                citation = citation_cd["citation"]
                citation_order = citation_cd["order"]
                citation_object = Citation(citation=citation)

                citation_objects.append(citation_object)
                sections.append(
                    {"content_object": citation_object, "order": citation_order}
                )

            image_objects = []
            for image_form in image_formset:
                image_cd = image_form.cleaned_data
                file = image_cd["file"]
                file_order = image_cd["order"]
                file_object = Image(file=file)

                image_objects.append(file_object)
                sections.append({"content_object": file_object, "order": file_order})

            try:
                with transaction.atomic():
                    post_tags = Tag.tags.add(*post_tags)
                    new_story.save()
                    new_story.tags.add(*post_tags)
                    title_object.save()
                    if len(subtitle_objects):
                        SubTitle.objects.bulk_create(subtitle_objects)
                    if len(text_objects):
                        Text.objects.bulk_create(text_objects)
                    if len(citation_objects):
                        Citation.objects.bulk_create(citation_objects)
                    if len(image_objects):
                        Image.objects.bulk_create(image_objects)
                    if len(sections):

                        def create_section(args_dict):
                            return Section(post=new_story, **args_dict)

                        sections = map(create_section, sections)
                        Section.objects.bulk_create(sections)
            except IntegrityError as e:
                print("Integrity error!", e)

                return render(
                    request,
                    "posts/post/write-story.html",
                    {
                        "blog": blog,
                        "post_form": post_form,
                        "title_form": title_form,
                        "subtitle_formset": subtitle_formset,
                        "text_formset": text_formset,
                        "citation_formset": citation_formset,
                        "image_formset": image_formset,
                    },
                )

            return redirect(reverse("posts:manage_posts", args=[blog.slug]))

    return render(
        request,
        "posts/post/write-story.html",
        {
            "blog": blog,
            "post_form": post_form,
            "title_form": title_form,
            "subtitle_formset": subtitle_formset,
            "text_formset": text_formset,
            "citation_formset": citation_formset,
            "image_formset": image_formset,
        },
    )
