from django.shortcuts import render
from django.http import HttpResponse
# def my_middleware(get_response):
#     print("one time initiallization")

#     def my_func(request):
#         print("this is  modified view")
#         response=render(request,"home.html")
#         print("this is modified view")
#         return response
#     return my_func


class MyMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("one time initiallization")

    def __call__(self, request):
        print("this is before view")
        response=self.get_response(request)
        print("this is after view")
        return response