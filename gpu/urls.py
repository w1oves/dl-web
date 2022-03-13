from django.urls import include, path
from . import views

urlpatterns = [
    # path("<str:User_name>", include("filelist.urls")),
    path("", views.index,name='gpuinfo')
]