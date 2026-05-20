from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    print("i am home view")
    return render(request,"home.html")

def another(request):
    return render(request,"another.html")