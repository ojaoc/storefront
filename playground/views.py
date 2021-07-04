# The views file is also misleading. This is a request handler

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# request -> response
# this has nothing to do with templates

def say_hello(request):
    return render(request, 'hello.html', {'name': 'Mosh'})
