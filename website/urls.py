from django.urls import path
from .views import Home,Compress,Rotate,Merge,Download

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path("compress/", Compress.as_view(), name="compress"),
    path("merge/", Merge.as_view(), name="merge"),
    path("rotate/", Rotate.as_view(), name="rotate"),
    path("download/<str:id>", Download.as_view(), name="download"),
]
