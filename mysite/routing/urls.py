from .views import *
from django.urls import path

urlpatterns = [
    path("simple_route/", simple_route),
    path("slug_route/<slug:slug>", slug_route), # r"^slug_route/(?P<slug>[0-9a-z-_]{1,16})/$"
    path("sum_route/<int:a>/<int:b>", sum_route),
    path("sum_get_method/?a=<int:a>&b=<int:b>/", sum_get_method),
    path("sum_post_method/", sum_post_method),
    path("extend_func/", extend_func),
    ]