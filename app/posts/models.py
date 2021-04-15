from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import OuterRef, Subquery
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from blogs.models import Blog
from common.utils import unique_slugify
from tags.models import Tag

from .fields import OrderField
from .utils import get_post_image_dir_path


class TitledQuerySet(models.QuerySet):
    def posts_with_title(self):
        return self.annotate(
            title=Subquery(
                Title.objects.filter(sections_relation__post=OuterRef("pk")).values(
                    "title"
                )
            )
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return TitledQuerySet(
            model=self.model, using=self._db, hints=self._hints
        ).posts_with_title()


class PublishedManager(PostManager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    slug = models.SlugField(max_length=255, unique_for_date="publish")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    tags = models.ManyToManyField(Tag, through="TaggedPost")

    objects = PostManager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return f"Post on {self.blog.title} blog"

    @property
    def first_text_section(self):
        text_id = ContentType.objects.get_for_model(Text).id
        citation_id = ContentType.objects.get_for_model(Citation).id
        text_section = (
            self.sections.filter(content_type__in=[text_id, citation_id])
            .order_by("order")
            .first()
        )
        if text_section:
            return text_section.content_object.content
        return None

    @property
    def first_image(self):
        image_id = ContentType.objects.get_for_model(Image).id
        image = self.sections.filter(content_type=image_id).order_by("order").first()
        if image:
            return image.content_object.content
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.get_title_section()["title"])
        super().save(*args, **kwargs)

    def get_title_section(self):
        title_id = ContentType.objects.get_for_model(Title).id
        title = self.sections.get(content_type=title_id)
        title_dict = {
            "title": title.content_object.content,
            "order": title.order,
        }
        return title_dict

    def get_subtitle_sections(self):
        subtitle_id = ContentType.objects.get_for_model(SubTitle).id
        subtitles = self.sections.filter(content_type=subtitle_id)
        subtitles_dict = [
            {"subtitle": s.content_object.content, "order": s.order} for s in subtitles
        ]
        return subtitles_dict

    def get_text_sections(self):
        text_id = ContentType.objects.get_for_model(Text).id
        texts = self.sections.filter(content_type=text_id)
        texts_dict = [
            {"text": t.content_object.content, "order": t.order} for t in texts
        ]
        return texts_dict

    def get_citation_sections(self):
        citation_id = ContentType.objects.get_for_model(Citation).id
        citations = self.sections.filter(content_type=citation_id)
        citations_dict = [
            {"citation": c.content_object.content, "order": c.order} for c in citations
        ]
        return citations_dict

    def get_image_sections(self):
        image_id = ContentType.objects.get_for_model(Image).id
        images = self.sections.filter(content_type=image_id)
        images_dict = [
            {"file": i.content_object.content, "order": i.order} for i in images
        ]
        return images_dict

    def get_absolute_url(self):
        return reverse(
            "posts:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class TaggedPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} tagged by {self.tag.name}"

    class Meta:
        unique_together = ("post", "tag")


class Section(models.Model):
    """
    Section
    """

    # POSTS_APP = 'posts'
    # Available section types
    SECTION_TYPES = (
        models.Q(app_label="posts", model="title")
        | models.Q(app_label="posts", model="subtitle")
        | models.Q(app_label="posts", model="text")
        | models.Q(app_label="posts", model="citation")
        | models.Q(app_label="posts", model="image")
    )

    # Every section is related to specific post
    post = models.ForeignKey(
        Post,
        related_name="sections",
        related_query_name="section",
        on_delete=models.CASCADE,
    )
    # Generic Foreign Key
    # table_id
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to=SECTION_TYPES
    )
    # row id
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    # Keeping track of post sections order
    order = OrderField(blank=True, for_fields=["post"])

    class Meta:
        unique_together = ("content_type", "object_id")
        ordering = ("order",)

    def __str__(self):
        return (
            f"post: {self.post.slug}, order: {self.order}, content: {self.content_type}"
        )


class ContentBase(models.Model):
    sections_relation = GenericRelation(
        Section,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="%(class)s",
    )

    @property
    def section(self):
        # Return the object if exists else None
        return self.sections_relation.first()

    @property
    def content(self):
        pass

    class Meta:
        abstract = True

    def __str__(self):
        return "ContentBase"

    def render(self):
        return render_to_string(
            f"posts/content/{self._meta.model_name}.html", {"item": self}
        )


class Title(ContentBase):
    title = models.TextField(max_length=50)

    @property
    def content(self):
        return self.title


class SubTitle(ContentBase):
    subtitle = models.TextField(max_length=100)

    @property
    def content(self):
        return self.subtitle


class Text(ContentBase):
    text = models.TextField()

    @property
    def content(self):
        return self.text


class Citation(ContentBase):
    citation = models.TextField()

    @property
    def content(self):
        return self.citation


class Image(ContentBase):
    file = models.ImageField(upload_to=get_post_image_dir_path)

    @property
    def content(self):
        return self.file
