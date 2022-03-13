from django.shortcuts import render
from .models import close_all_runner
from dl2.models import User


def index(request):

    if "user" in request.COOKIES:
        User_name = request.COOKIES["user"]
    else:
        User_name = "default"
    user = User.objects.get(name=User_name)
    context = {}
    callback = {}
    
    runners = [user.trainrunner_set.all(), user.testrunner_set.all()]
    # 不同模型得到的QuerySet不可以进行归并
    for qs in runners:
        for runner in qs:
            callback.update(runner.get_buttons()["callback"])
    if request.POST:
        for option in request.POST.getlist("runner_buttons"):
            if option and option in callback:
                callback[option]()
        if "close_all" in request.POST:
            close_all_runner(user)
    runners = [user.trainrunner_set.all(), user.testrunner_set.all()]
    train_info = []
    test_info=[]
    for runner in user.trainrunner_set.all():
        train_info.append(runner.get_context())
    for runner in user.testrunner_set.all():
        test_info.append(runner.get_context())
    context["train_runners"] = train_info
    context["test_runners"] = test_info
    return render(request, "runner.html", context)
