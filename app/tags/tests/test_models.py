from django.test import TestCase

from model_bakery import baker

from tags.models import Tag


class TaggedItemModelTestCase(TestCase):
    def setUp(self):
        self.blog_1 = baker.make('Blog')
        self.post_1 = baker.make('Post', blog=self.blog_1)
        self.post_2 = baker.make('Post', blog=self.blog_1)

    def test_add_tags_as_objects(self):
        Tag.objects.get_or_create(name='tag1')
        Tag.objects.get_or_create(name='tag2')
        Tag.objects.get_or_create(name='tag3')
        Tag.objects.get_or_create(name='tag3')

        self.assertEqual(Tag.objects.count(), 3)

    def test_add_tags_as_strings(self):
        tags = Tag.tags.add('tag1', 'tag2', 'tag3', 'tag3')

        self.post_1.tags.add(*tags)
        self.post_2.tags.add(*tags)
        self.blog_1.tags.add(tags[0])

        self.assertEqual(self.post_1.tags.count(), 3)
        self.assertEqual(self.post_2.tags.count(), 3)
        self.assertEqual(self.blog_1.tags.count(), 1)

    def test_remove_tags_as_strings(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.assertEqual(Tag.objects.count(), 3)

        Tag.tags.remove('tag2', 'tag3', 'tag4')

        self.assertEqual(Tag.objects.count(), 1)

    def test_remove_nonexisting_tag(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.assertEqual(Tag.objects.count(), 3)

        Tag.tags.remove('tag4')

        self.assertEqual(Tag.objects.count(), 3)

    def test_tag_blog_and_post(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.post_1.tags.add(*tags)
        self.post_2.tags.add(*tags[1:])
        self.blog_1.tags.add(tags[0])

        self.assertEqual(self.post_1.tags.count(), 3)
        self.assertEqual(self.post_2.tags.count(), 2)
        self.assertEqual(self.blog_1.tags.count(), 1)

    def test_remove_tags_from_blog_and_post(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.post_1.tags.add(*tags)
        self.post_2.tags.add(*tags)
        self.blog_1.tags.add(tags[0], tags[1])

        self.post_1.tags.remove(*tags)
        self.post_2.tags.remove(tags[0], tags[1])
        self.blog_1.tags.remove(tags[2])

        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(self.post_1.tags.count(), 0)
        self.assertEqual(self.post_2.tags.count(), 1)
        self.assertEqual(self.blog_1.tags.count(), 2)

    def test_check_if_tag_cascade_when_removed(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.assertEqual(Tag.objects.count(), 3)
        self.post_1.tags.add(*tags)
        self.assertEqual(Tag.objects.count(), 3)
        Tag.tags.remove('tag1')
        self.assertEqual(self.post_1.tags.count(), 2)
        self.assertEqual(Tag.objects.count(), 2)

    def test_check_if_tag_gets_removed_when_not_used_anymore(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.assertEqual(Tag.objects.count(), 3)

        self.post_1.tags.add(*tags)
        self.post_1.tags.remove(tags[0])

        self.assertEqual(self.post_1.tags.count(), 2)
        self.assertEqual(Tag.objects.count(), 2)

    def test_check_if_tag_is_not_removed_when_blog_is_still_tagged(self):
        tags = ['tag1', 'tag2', 'tag3']
        tags = Tag.tags.add(*tags)

        self.assertEqual(Tag.objects.count(), 3)

        self.post_1.tags.add(*tags)
        self.blog_1.tags.add(tags[0])

        self.assertEqual(self.post_1.tags.count(), 3)
        self.assertEqual(self.blog_1.tags.count(), 1)

        self.post_1.tags.remove(tags[0])

        self.assertEqual(self.post_1.tags.count(), 2)
        self.assertEqual(self.blog_1.tags.count(), 1)
        self.assertEqual(Tag.objects.count(), 3)
