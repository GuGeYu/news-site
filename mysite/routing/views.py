from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render


@require_GET
def simple_route(request):
    return HttpResponse("", status="200")


def slug_route(request, slug):
    if 1 <= len(slug) <= 16:
        return HttpResponse(slug)
    else:
        return HttpResponse(status="404")


def sum_route(request, a, b):
    return HttpResponse(a + b)


@require_GET
def sum_get_method(request, a, b):
    return HttpResponse(a + b)


@require_POST
def sum_post_method(request, a, b):
    return HttpResponse(a + b)


def extend_func(request):
    context = {'a': 1,
               'b': 2,
               }
    return render(request, 'extend.html', context=context)

