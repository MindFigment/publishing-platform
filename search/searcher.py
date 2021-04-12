from django.apps import apps
from django.db.models import Sum
from django.db.models.functions import Greatest

from django.contrib.postgres.search import TrigramSimilarity

from itertools import chain
from operator import attrgetter


class Searcher:
    def __init__(self, query_string, search_model, uni_fields=[], agg_fields=[], similarity_threshold=0.1):
        self.query_string = query_string
        self.search_model = search_model
        self.uni_fields = uni_fields
        self.agg_fields = agg_fields
        self.n = len(self.uni_fields) + len(self.agg_fields)
        self.similarity_threshold = similarity_threshold

        self.model = apps.get_model(self.search_model)
        self.queryset = None

    def get_queryset(self):
        if self.queryset is None:
            self._build_queryset()
        return self.queryset

    def most_similar(self, n):
        if self.queryset is None:
            self._build_queryset()
        return self.queryset[:n]

    def _build_queryset(self):
        self.queryset = self.model._default_manager.annotate(
            max_similarity=self._build_max_similarity()
        ).filter(max_similarity__gt=self.similarity_threshold).order_by('-max_similarity')

    def _build_max_similarity(self):
        if self.n > 1:
            return Greatest(*self._trig_similarities())
        return self._trig_similarities()[0]

    def _trig_similarities(self):
        trig_similarities = [
            TrigramSimilarity(f'{field}', f'{self.query_string}') for field in self.uni_fields
        ]
        trig_similarities += [
            Sum(TrigramSimilarity(f'{field}', f'{self.query_string}')) for field in self.agg_fields
        ]
        return trig_similarities
