from django.apps import apps
from django.db.models import Sum
from django.db.models.functions import Greatest

from django.contrib.postgres.search import TrigramSimilarity

from itertools import chain
from operator import attrgetter


class Searcher:
    def __init__(self, query_string, search_model, uni_fields=[], agg_fields=[]):
        self.query_string = query_string
        self.search_model = search_model
        self.uni_fields = uni_fields
        self.agg_fields = agg_fields
        self.n = len(self.uni_fields) + len(self.agg_fields)

        # self.models = tuple(apps.get_model(m) for m in search_models)
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

    def merge_into_list(self, *others):
        my_queryset = self.get_queryset()
        other_querysets = [other.get_queryset() for other in others]
        result_list = sorted(
            chain(my_queryset, *other_querysets),
            key=attrgetter('max_similarity'),
            reverse=True
        )
        return result_list

    def _build_queryset(self):
        self.queryset = self.model._default_manager.annotate(
            max_similarity=self._build_max_similarity()
        ).filter(max_similarity__gt=0.01).order_by('-max_similarity')

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
