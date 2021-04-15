import re
from itertools import chain

from django.db.models import Q


def build_query(obj):
    query = " ".join([obj.title] + [tag.name for tag in obj.tags.all()])
    return query


def get_search_params(cd):
    AGG_FIELDS_LIST = ["tags__name"]

    query = cd["query"]
    search_models = (
        cd["search_models"] if cd.get("search_models", None) else cd["search_model"]
    )
    search_fields = cd["search_fields"]
    uni_fields = []
    agg_fields = []
    for field in search_fields:
        if field not in AGG_FIELDS_LIST:
            uni_fields.append(field)
        else:
            agg_fields.append(field)
    return query, search_models, uni_fields, agg_fields


######################################################################
# FUNCTIONS NOT USED RIGHT NOW -> REPLACED BY POSTGRES TRISIMILARITY #
######################################################################


def get_search_query(query_string, by):
    query_terms = get_query_terms(query_string)
    query = None
    for term in query_terms:
        print("query:", term)
        or_query = None
        for field_name in by:
            q = Q(**{f"{field_name}__icontains": term})
            or_query = q if or_query is None else or_query | q
        query = or_query if query is None else query | or_query
    return query


def get_ngrams(query_string, n=3):
    idxs = [i for i in range(0, len(query_string) + n, n)]
    if len(query_string) <= n:
        yield query_string
    else:
        for i, start in enumerate(idxs):
            for end in idxs[i + 1 :]:
                gram = query_string[start:end]
                if len(gram) >= n:
                    yield gram


def normalize_query(
    query_string,
    findterms=re.compile(r'"([\w\s,]+)"|(\w+)').findall,
    normspaces=re.compile(r"\s{2,}").sub,
):
    query_string = query_string.strip().lower()
    return [normspaces(" ", (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query_terms(query_string):
    normalized_query = normalize_query(query_string)
    query_terms = chain(*(get_ngrams(q) for q in normalized_query))
    return query_terms
