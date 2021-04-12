from django.shortcuts import render

from .searcher import Searcher
from .forms import SearchForm
from .utils import get_search_params


def search_blogs_and_posts(request):
    search_form = SearchForm()
    query = None
    post_results = []
    blog_results = []
    search_posts = False
    search_blogs = False

    if request.GET.get('query', None):
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            cd = search_form.cleaned_data
            query, search_models, uni_fields, agg_fields = get_search_params(
                cd
            )

            if SearchForm.SEARCH_POSTS in search_models:
                post_searcher = Searcher(
                    query, SearchForm.SEARCH_POSTS, uni_fields, agg_fields
                )
                post_results = post_searcher.most_similar(20)
                search_posts = True

            if SearchForm.SEARCH_BLOGS in search_models:
                blog_searcher = Searcher(
                    query, SearchForm.SEARCH_BLOGS, uni_fields, agg_fields
                )
                blog_results = blog_searcher.most_similar(20)
                search_blogs = True

    return render(request,
                  'search/search.html',
                  {
                      'search_form': search_form,
                      'query': query,
                      'post_results': post_results,
                      'blog_results': blog_results,
                      'n_posts': len(post_results),
                      'n_blogs': len(blog_results),
                      'search_posts': search_posts,
                      'search_blogs': search_blogs,
                  })
