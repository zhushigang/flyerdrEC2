from django.shortcuts import render
from django.http import HttpResponse

def index(req):
  return render(req, 'pointstracker/index.html', {'some_variable': 'some_value'})
