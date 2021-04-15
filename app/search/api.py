import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from common.encoders import ExtendedEncoder
from posts.models import Post

from .searcher import Searcher
from .utils import build_query


@require_http_methods(["GET"])
def get_most_similar_posts(request):
    slug = request.GET.get("slug")
    n = int(request.GET.get("n"))

    post = get_object_or_404(Post.objects.all(), slug=slug)

    query = build_query(post)
    search_model = "posts.Post"
    uni_fields = ["title"]
    agg_fields = ["tags__name"]

    searcher = Searcher(query, search_model, uni_fields, agg_fields)
    # We pass n + 1, because one of the posts will be the post
    # we are searching against
    similar_posts = searcher.most_similar(n + 1)
    similar_posts = [
        json.dumps(p, cls=ExtendedEncoder)
        for p in similar_posts
        if p.id != post.id and p.status == "published"
    ]

    return JsonResponse(similar_posts, safe=False)
