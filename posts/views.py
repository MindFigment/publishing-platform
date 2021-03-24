from django.core.checks.messages import Error
from django.db.utils import IntegrityError
from blogs.views import blog_ajax_list
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import modelform_factory, modelformset_factory
from django.apps import apps
from django.urls.base import reverse
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from .models import Citation, Image, Post, Section, Title, SubTitle, Text
from blogs.models import Blog
from .forms import TitleForm, SubTitleFormset, TextFormset, CitationFormset, ImageFormset
from common.utils import unique_slugify


# WRITE_STORY_ROUTER = {
#     'GET':
# }
SUBTITLE_PREFIX = 'subtitle'
TEXT_PREFIX = 'text'
CITATION_PREFIX = 'citation'
IMAGE_PREFIX = 'image'


def create_post(request, blog_id):
    blog = get_object_or_404(Blog.objects.all(), pk=blog_id)

    if request.method == 'GET':
        print('\n\n\nGET\n', request.GET, '\n\n\n')
        title_form = TitleForm()
        subtitle_formset = SubTitleFormset(prefix=SUBTITLE_PREFIX)
        text_formset = TextFormset(prefix=TEXT_PREFIX)
        citation_formset = CitationFormset(prefix=CITATION_PREFIX)
        image_formset = ImageFormset(prefix=IMAGE_PREFIX)
    elif request.method == 'POST':
        print('\n\n\nPOST\n', request.POST, request.FILES, '\n\n\n')
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
        if title_form.is_valid() and subtitle_formset.is_valid() and text_formset.is_valid() and image_formset.is_valid() and citation_formset.is_valid():
            # Create post
            new_story = Post(blog=blog)
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
                    new_story.save()
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
                              'posts/manage/post/write_story.html',
                              {'blog': blog,
                               'title_form': title_form,
                               'subtitle_formset': subtitle_formset,
                               'text_formset': text_formset,
                               'citation_formset': citation_formset,
                               'image_formset': image_formset})

            return redirect(reverse('blogs:manage_blogs'))

        print('Ups, something went wrong!\n', image_formset)

    print('\nrendering\n')
    return render(request,
                  'posts/manage/post/write_story.html',
                  {'blog': blog,
                   'title_form': title_form,
                   'subtitle_formset': subtitle_formset,
                   'text_formset': text_formset,
                   'citation_formset': citation_formset,
                   'image_formset': image_formset})


class PostSectionListView(TemplateResponseMixin, View):
    template_name = 'posts/manage/post/section_list.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post,
                                 id=post_id)
        return self.render_to_response({'post': post})


class SectionCreateUpdateView(TemplateResponseMixin, View):
    p = None
    model = None
    obj = None
    template_name = 'posts/manage/section/form.html'

    def get_model(self, model_name):
        print('\n\nGET MODEL', model_name)
        if model_name in ['text', 'video', 'image']:
            return apps.get_model(app_label='posts',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        print('GET FORM')
        Form = modelform_factory(
            model, exclude=['onwer', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, post_id, model_name, id=None):
        print('DISPATCH')
        self.p = get_object_or_404(Post,
                                   id=post_id)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id)
        return super().dispatch(request, post_id, model_name, id)

    def get(self, request, post_id, model_name, id=None):
        print(request)
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, post_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.p = post_id
            obj.save()
            if not id:
                # new section
                Section.objects.create(post=self.p, item=obj)
        return redirect('posts:post_section_list', self.p.id)


class SectionDeleteView(View):
    def post(self, request, id):
        section = get_object_or_404(Section,
                                    id=id)
        post_ = section.post
        section.item.delete()
        section.delete()
        return redirect('posts:post_section_list', post_.id)


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
                  'posts/manage/post/detail.html',
                  {'post': post})
