from django.test import TestCase
from model_bakery import baker

from blogs.models import FollowRelationship


class FollowRelationshipTestCase(TestCase):
    def setUp(self):
        self.author = baker.make("Profile", user__email="a@gmail.com")

        self.profile_1 = baker.make("Profile", user__email="b@gmail.com")
        self.profile_2 = baker.make("Profile", user__email="c@gmail.com")
        self.profile_3 = baker.make("Profile", user__email="d@gmail.com")
        self.profile_4 = baker.make("Profile", user__email="e@gmail.com")
        self.profile_5 = baker.make("Profile", user__email="f@gmail.com")

        self.blog_1 = baker.make("Blog", title="title1", author=self.author)
        self.blog_2 = baker.make("Blog", title="title2", author=self.author)

        FollowRelationship.objects.bulk_create(
            [
                # Followers for blog 1
                FollowRelationship(
                    blog=self.blog_1, profile=self.profile_1, seen=False
                ),
                FollowRelationship(
                    blog=self.blog_1, profile=self.profile_2, seen=False
                ),
                FollowRelationship(blog=self.blog_1, profile=self.profile_3, seen=True),
                FollowRelationship(blog=self.blog_1, profile=self.profile_4, seen=True),
                FollowRelationship(blog=self.blog_1, profile=self.profile_5, seen=True),
                # Followers for blog 2
                FollowRelationship(blog=self.blog_2, profile=self.profile_1, seen=True),
                FollowRelationship(
                    blog=self.blog_2, profile=self.profile_2, seen=False
                ),
                FollowRelationship(
                    blog=self.blog_2, profile=self.profile_3, seen=False
                ),
            ]
        )

    def test_followers_properly_added(self):
        self.assertEqual(self.blog_1.followers.count(), 5)
        self.assertEqual(self.blog_2.followers.count(), 3)

    def test_seen_followers_retrieved(self):
        seen_followers_1 = self.blog_1.get_old_followers()
        self.assertEqual(seen_followers_1.count(), 3)

        seen_followers_2 = self.blog_2.get_old_followers()
        self.assertEqual(seen_followers_2.count(), 1)

    def test_notseen_followers_retrieved(self):
        notseen_followers_1 = self.blog_1.get_new_followers()
        self.assertEqual(notseen_followers_1.count(), 2)

        notseen_followers_2 = self.blog_2.get_new_followers()
        self.assertEqual(notseen_followers_2.count(), 2)

    def test_set_seen_followers_as_seen(self):
        seen_followers = self.blog_1.get_old_followers()
        self.assertEqual(seen_followers.count(), 3)
        self.blog_1.set_followers_as_old(seen_followers)

        seen_followers_ = self.blog_1.get_old_followers()
        self.assertEqual(seen_followers_.count(), 3)

    def test_set_notseen_followers_as_seen(self):
        notseen_followers = self.blog_1.get_new_followers()
        seen_followers = self.blog_1.get_old_followers()
        self.assertEqual(seen_followers.count(), 3)
        self.assertEqual(notseen_followers.count(), 2)
        self.blog_1.set_followers_as_old(notseen_followers)

        seen_followers = self.blog_1.get_old_followers()
        notseen_followers = self.blog_1.get_new_followers()
        self.assertEqual(seen_followers.count(), 5)
        self.assertEqual(notseen_followers.count(), 0)
