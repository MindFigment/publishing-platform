from django.shortcuts import render

from .models import Searcher
from .forms import SearchForm
from .utils import get_search_params


def search(request):
    search_form = SearchForm()
    query = None
    results = None
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            cd = search_form.cleaned_data
            query, search_models, uni_fields, agg_fields = get_search_params(
                cd)
            searchers = [Searcher(query, model, uni_fields, agg_fields)
                         for model in search_models]
            results = searchers[0].most_similar(20) if len(
                searchers) == 1 else searchers[0].merge_into_list(*searchers[1:])
    return render(request,
                  'search/search.html',
                  {
                      'search_form': search_form,
                      'query': query,
                      'results': results
                  })
