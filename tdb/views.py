from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views import generic
from .models import TDB, close_all_tdb
from django.utils.decorators import classonlymethod
from dl2.models import User

# Create your views here.
class IndexView(generic.ListView):
    template_name = "tdb.html"
    context_object_name = "TDBs"
    model = TDB

    def get(self, request):
        if "user" in request.COOKIES:
            User_name = request.COOKIES["user"]
        else:
            User_name = "default"
        user = User.objects.get(name=User_name)
        tdbs = user.tdb_set.all()
        print(tdbs)
        return render(request, "tdb.html", {"TDBs": tdbs})

    def post(self, request):
        if "close_all" in request.POST:
            if "user" in request.COOKIES:
                User_name = request.COOKIES["user"]
            else:
                User_name = "default"
            user = User.objects.get(name=User_name)
            close_all_tdb(user)
        return redirect(reverse("tdb"))
