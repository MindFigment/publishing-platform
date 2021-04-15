import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import InvalidPage, Paginator, EmptyPage, PageNotAnInteger

from blogs.models import Blog
from common.encoders import ExtendedEncoder


@require_http_methods(['GET'])
def get_detailed_blogs(request):
    print(request.GET)
    page = request.GET.get('page')
    n = request.GET.get('n')
    blogs = Blog.active.all()
    paginator = Paginator(blogs, n)

    try:
        blogs = paginator.page(page)
        print('1')
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        blogs = paginator.page(1)
        print('2')
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
        return JsonResponse({'empty': True})
    except InvalidPage:
        blogs = paginator.page(1)
        print('4')

    blogs = [json.dumps(b, cls=ExtendedEncoder) for b in blogs]
    return JsonResponse(blogs, safe=False)
