from django.shortcuts import render
from django.http import HttpResponse
import random


def test(request):
    return HttpResponse("Hello World")

def main_page_view(request):
    return render(request, 'base.html')