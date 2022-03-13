from django.urls import include, path
from . import views

urlpatterns = [
    # path("<str:User_name>", include("filelist.urls")),
    path("", views.index, {"option": "gpu"}),
    path("index/", views.index, {"option": "gpu"}),
    path("workdir/", views.index, {"option": "workdir"}),
    path("configdir/", views.index, {"option": "configdir"}),
    path("gpu/", views.index, {"option": "gpu"}),
    path("tdb/", views.index, {"option": "tdb"}),
    path("runner/", views.index, {"option": "runner"}),
]
