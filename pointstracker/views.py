from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pointstracker import models
from pointstracker import queue
from pointstracker import get_balance

def index(req):
  return render(req, 'pointstracker/index.html', {})

def login(req):
  if req.method == "POST":
    if "username" in req.POST and "password" in req.POST:
      uname = req.POST['username']
      password = req.POST['password']
      user = auth.authenticate(username=uname, password=password)
      if user is not None and user.is_active:
        auth.login(req, user)
        return redirect(req.GET['next'] if 'next' in req.GET else 'main')
    messages.warning(req, 'Username and password did not match.')
  return render(req, 'pointstracker/login.html', {})

def signup(req):
  if (req.method == "POST" and
      all(x in req.POST and req.POST[x] != "" for x in
      ("email", "password", "password2", "last", "first"))):
    email = req.POST['email']
    password1 = req.POST['password']
    password2 = req.POST['password2']
    if forms.EmailField().clean(email) and password1==password2:
      new_user = User.objects.create_user(email, email, password1)
      new_user.first_name = req.POST['first']
      new_user.last_name = req.POST['last']
      new_user.save()
      return redirect('main')
    last = req.POST['last']
  return render(req, 'pointstracker/signup.html', {})

@login_required
def manage(req):
  if req.method=='GET':
    json = get_balance.get_balance(req.user)
    return render(req, 'pointstracker/manage.html', json)
    
  elif req.method=='POST':
    if "id" in req.POST and "password" in req.POST:
      id = req.POST['id']
      password = req.POST['password']
      program_shortname = req.POST['shortname']
      program = models.RewardsProgram.objects.get(shortname=program_shortname)
      value_pairs = {'cred1':id,'cred2':password}
      new_RewardsProgramAccount, created = models.RewardsProgramAccount.objects.update_or_create(user=req.user, rewards_program=program,defaults=value_pairs)
      new_RewardsProgramAccount.save()
    return redirect('manage')
	
	
def about(req):
  return render(req, 'pointstracker/about.html', {})

def main(req):
  return render(req, 'pointstracker/main.html', {})

