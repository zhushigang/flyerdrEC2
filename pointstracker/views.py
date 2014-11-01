from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import auth
from pointstracker import models

def index(req):
  return render(req, 'pointstracker/index.html', {})

def login(req):
  if req.method == "POST" and "username" in req.POST and "password" in req.POST:
    uname = req.POST['username']
    password = req.POST['password']
    user = auth.authenticate(username=uname, password=password)
    if user is not None and user.is_active:
      auth.login(req, user)
      return redirect('main')
  return render(req, 'pointstracker/login.html', {})

def signup(req):
  return render(req, 'pointstracker/signup.html', {})

def manage(req):
  return render(req, 'pointstracker/manage.html', {})

def about(req):
  return render(req, 'pointstracker/about.html', {})

def main(req):
  return render(req, 'pointstracker/main.html', {})

