from django.test import TestCase
from model_bakery import baker

from search.searcher import Searcher
from search.utils import get_ngrams, normalize_query
from tags.models import Tag


class NormalizeQueryTestCase(TestCase):
    def setUp(self):
        self.query_1 = "Rise and Fall of Networks"
        self.query_2 = 'Rise    and "Fall of Networks"'
        self.query_3 = '"Deep Code", music, fragility, ha ha'
        self.query_4 = '"music fragility", deep code"'

    def test_normalize_query(self):
        query_1_normalized = normalize_query(self.query_1)
        self.assertEqual(query_1_normalized, ["rise", "and", "fall", "of", "networks"])

        query_2_normalized = normalize_query(self.query_2)
        self.assertEqual(query_2_normalized, ["rise", "and", "fall of networks"])

        query_3_normalized = normalize_query(self.query_3)
        self.assertEqual(
            query_3_normalized, ["deep code", "music", "fragility", "ha", "ha"]
        )

        query_4_normalized = normalize_query(self.query_4)
        self.assertEqual(query_4_normalized, ["music fragility", "deep", "code"])


class NGramsTestCase(TestCase):
    def setUp(self):
        self.query_1 = "net"
        self.query_2 = "networks"
        self.query_3 = "ntworks"
        self.query_4 = "fragility"
        self.query_5 = "nets"

    def test_3grams(self):
        query_3grams_1 = list(get_ngrams(self.query_1))
        self.assertEqual(query_3grams_1, ["net"])

        query_3grams_5 = list(get_ngrams(self.query_5))
        self.assertEqual(query_3grams_5, ["net", "nets"])

        query_3grams_2 = list(get_ngrams(self.query_2))
        self.assertEqual(
            query_3grams_2, ["net", "networ", "networks"] + ["wor", "works"]
        )

        query_3grams_3 = list(get_ngrams(self.query_3))
        self.assertEqual(query_3grams_3, ["ntw", "ntwork", "ntworks"] + ["ork", "orks"])

        query_3grams_4 = list(get_ngrams(self.query_4))
        self.assertEqual(
            query_3grams_4, ["fra", "fragil", "fragility"] + ["gil", "gility"] + ["ity"]
        )


class SearcherTestCase(TestCase):
    def setUp(self):
        self.blog_1 = baker.make(
            "Blog", title="Deep Neural Networks", author__user__email="a@gmail.com"
        )
        self.blog_2 = baker.make(
            "Blog", title="Rise and Fall of Networks", author__user__email="b@gmail.com"
        )

    def test_title_similarity(self):
        tags = ["rise", "fall", "of", "networks", "random"]
        tags = Tag.tags.add(*tags)

        self.blog_1.tags.add(*tags)
        self.blog_2.tags.add(*tags)

        querystring = "Rise and Fall"
        searcher_1 = Searcher(querystring, "blogs.Blog", ["title"], [])

        searcher_2 = Searcher(querystring, "blogs.Blog", ["title"], ["tags__name"])

        max_1 = searcher_1.most_similar(1).values("max_similarity")[0]["max_similarity"]
        max_2 = searcher_2.most_similar(1).values("max_similarity")[0]["max_similarity"]

        self.assertGreater(max_2, max_1)
