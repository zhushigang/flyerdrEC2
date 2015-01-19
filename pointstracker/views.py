from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
import json

from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.views.decorators.csrf import csrf_exempt
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
  
@csrf_exempt
def login_api(req):
  uname = req.POST['username']
  password = req.POST['password']
  user = auth.authenticate(username=uname, password=password)
  if user is not None and user.is_active:
    userid = user.get_username()
    set = {'userid': userid}
    data = json.dumps(set)
    return HttpResponse(data, content_type='application/json')
  response = HttpResponse()
  response.status_code = 201
  return response

def reset(req):
  return password_reset(req, post_reset_redirect='index')
  
def reset_confirm(req, uidb64=None, token=None):
  return password_reset_confirm(req, 
        uidb64=uidb64, token=token, post_reset_redirect='login')
  
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

@csrf_exempt
def rp_api(req):
  user = User.objects.get(username=req.POST['username'])
  accounts = list(models.RewardsProgramAccount.objects.filter(user=user))
  sets = list()
  for account in accounts:
    set = dict()
    set['shortname'] = account.rewards_program.shortname
    set['cardnumber'] = account.cred1
    set['displayname'] = account.rewards_program.displayname
    sets+=[set]
  
  data = json.dumps(sets)
  return HttpResponse(data, content_type='application/json')

@csrf_exempt
def credit_api(req):
  user = User.objects.get(username='zhushigang@gmail.com')
  rp = models.RewardsProgram.objects.get(shortname='aa')
  account = models.RewardsProgramAccount.objects.get(user=user, rewards_program=rp)
  cardnumber = account.cred1
  balances = get_balance.get_balance(user)
  balance = balances['aa']
  set = {'cardnumber':cardnumber, 'balance':balance}
  data = json.dumps(set)
  return HttpResponse(data, content_type='application/json')

@csrf_exempt
def add_api(req):
  user = User.objects.get(username=req.POST['username'])
  id = req.POST['cardnumber']
  password = req.POST['password']
  program_shortname = req.POST['shortname']
  program = models.RewardsProgram.objects.get(shortname=program_shortname)
  value_pairs = {'cred1':id,'cred2':password}
  new_RewardsProgramAccount, created = models.RewardsProgramAccount.objects.update_or_create(user=user, rewards_program=program,defaults=value_pairs)
  new_RewardsProgramAccount.save()
  response = HttpResponse()
  response.status_code = 200
  return response
  

  
@csrf_exempt
def test(req):
  set = {'status':200}
  data = json.dumps(set)
  post = req.POST
  data = json.dumps(post)
  response = HttpResponse(data, content_type='application/json')
  response.status_code = 201
  return response

@csrf_exempt
def signup_api(req):
  
  email = req.POST['email']
  password = req.POST['password']
  
  
  #user exists
  if User.objects.filter(username=email).count():
    set = {'userid': 'exist'}
    data = json.dumps(set)
    response = HttpResponse()
    response.status_code = 201
    return HttpResponse(data, content_type='application/json')
  new_user = User.objects.create_user(email, email, password)
  new_user.first_name = req.POST['first']
  new_user.last_name = req.POST['last']
  new_user.save()
  set = {'userid': email}
  data = json.dumps(set)
  return HttpResponse(data, content_type='application/json')



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
      queue.refresh_rewards_balance(new_RewardsProgramAccount)
    return redirect('manage')
	
	
def about(req):
  return render(req, 'pointstracker/about.html', {})

def main(req):
  return render(req, 'pointstracker/main.html', {})

