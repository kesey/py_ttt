from django.shortcuts import render
# from django.core.paginator import Paginator

def home(request):
    return render(
        request,
        "ttt_front/home.html"
    )
