from django.shortcuts import render

# Create your views here.
from .gpu_info import get_gpu_info
def index(request):
    context={}
    context["gpu_info"] = get_gpu_info()
    return render(request, "gpu/gpuinfo.html", context)