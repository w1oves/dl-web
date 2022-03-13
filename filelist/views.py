from django.shortcuts import render

from filelist.models import Machine
from .forms import FileListForm
from dl2.models import User
import os.path as osp
from tdb.models import create_tdb
from runner.models import train, test
from gpu.gpu_info import get_gpu_simple_info
from collections import deque

# Create your views here.
def work_dir(
    request,
):
    if "user" in request.COOKIES:
        User_name = request.COOKIES["user"]
    else:
        User_name = "default"
    context = {}
    user = User.objects.get(name=User_name)
    path = user.work_dir
    context["button_text"] = "创建Tensorboard"
    try:
        m = user.machine_set.get(category="work_dir")
    except:
        m = user.machine_set.create(
            category="work_dir",
            root_path=path,
            cur_dir=path,
            cur_file=path,
        )
    if request.method == "POST":
        if "enter_path" in request.POST:
            m.enter_path(request.POST["enter_path"])
        if "test" in request.POST or "aug_test" in request.POST:
            paths = request.POST.getlist("select_paths")
            config = list(filter(lambda x: x[-3:] == ".py", paths))[0]
            weight = list(filter(lambda x: x[-4:] == ".pth", paths))[0]
            gpus = request.POST.get("gpus")
            aug_test = "aug_test" in request.POST
            test(user, config, gpus, weight, aug_test)
        if "tensorboard" in request.POST:
            paths = request.POST.getlist("select_paths")
            create_tdb(user, paths)
    user.save()
    m.save()
    if osp.isfile(m.cur_file):
        with open(m.cur_file, "r", encoding="utf-8") as f:
            try:
                lines = f.readlines()
                context["content"] = "".join(lines)
            except:
                context["content"] = "code error"
    choices = m.get_choices()
    context["choices"] = choices
    context["debug"] = request
    context["gpus"] = get_gpu_simple_info()
    return render(request, "work_dir.html", context)


# Create your views here.
def config_dir(
    request,
):
    if "user" in request.COOKIES:
        User_name = request.COOKIES["user"]
    else:
        User_name = "default"
    context = {}
    user = User.objects.get(name=User_name)
    path = user.config_dir
    context["button_text"] = "训练"
    try:
        m = user.machine_set.get(category="config_dir")
    except:
        m = user.machine_set.create(
            category="config_dir",
            root_path=path,
            cur_dir=path,
            cur_file=path,
        )
    if request.method == "POST":
        if "enter_path" in request.POST:
            m.enter_path(request.POST["enter_path"])
        if "select_paths" in request.POST:
            paths = request.POST.getlist("select_paths")
            gpus = ",".join(request.POST.getlist("gpus"))
            train(user, paths[0], gpus)
    user.save()
    m.save()
    if osp.isfile(m.cur_file):
        with open(m.cur_file, "r", encoding="utf-8") as f:
            try:
                context["content"] = "".join(f.readlines())
            except:
                context["content"] = "code error"
    choices = m.get_choices()
    context["choices"] = choices
    context["debug"] = request
    context["gpus"] = get_gpu_simple_info()
    return render(request, "config_dir.html", context)
