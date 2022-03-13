from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView
from django.urls import reverse
from .forms import UserForm
from .models import User


class IndexView(generic.ListView):
    template_name = "dl2/index.html"
    context_object_name = "Users"
    model = User

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by("-name")


def login(request, user):
    response = redirect("/watch")
    response.set_cookie("user", user)
    return response


def signup(request):
    # 如果form通过POST方法发送数据
    context = {}
    if request.method == "POST":
        # 接受request.POST参数构造form类的实例
        form = UserForm(request.POST)
        # 验证数据是否合法
        if form.is_valid():
            # 处理form.cleaned_data中的数据
            # ...
            # 重定向到一个新的URL
            # form.save()
            form.save()
            return redirect(reverse("login"))
        else:
            context["message"] = "输入信息不正确"

    # 如果是通过GET方法请求数据，返回一个空的表单
    else:
        form = UserForm()
    context["form"] = form

    return render(request, "dl2/signup.html", context)
