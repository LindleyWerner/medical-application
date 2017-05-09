from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse

def index(request):
    return render(request, 'core_app/index.html')


def about(request):
    return render(request, 'core_app/about.html')