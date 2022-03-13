from django.urls import include, path
from . import views
from tdb.models import create_tdb

urlpatterns = [
    path(
        "workdir/",
        views.work_dir,
        name="workdir",
    ),
    path("configdir/", views.config_dir, name="configdir"),
]
