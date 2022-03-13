from django.shortcuts import render


def index(request, option):
    if "user" in request.COOKIES:
        User_name = request.COOKIES["user"]
    else:
        User_name = "default"
    context = {"User_name": User_name, "option": option}
    return render(request, "watch/index.html", context)
