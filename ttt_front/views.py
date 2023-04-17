from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

def home(request):
    return render(
        request,
        "ttt_front/home.html"
    )
