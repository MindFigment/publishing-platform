import json

from django.core.paginator import (EmptyPage, InvalidPage, PageNotAnInteger,
                                   Paginator)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from common.encoders import ExtendedEncoder
from posts.models import Post


@require_http_methods(["GET"])
def get_detailed_posts(request):
    page = request.GET.get("page")
    n = request.GET.get("n")
    posts = Post.published.all()
    paginator = Paginator(posts, n)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        return JsonResponse({"empty": True})
    except InvalidPage:
        posts = paginator.page(1)

    posts = [json.dumps(p, cls=ExtendedEncoder) for p in posts]
    return JsonResponse(posts, safe=False)
