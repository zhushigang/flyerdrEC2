from django.db import models
from django.contrib.auth.models import User

class RewardsProgram(models.Model):
  shortname = models.CharField(max_length=32, unique=True)
  displayname = models.CharField(max_length=255)
  created_time = models.DateTimeField(auto_now_add=True, editable=False)
  updated_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)

class RewardsProgramAccount(models.Model):
  user = models.ForeignKey(User)
  rewards_program = models.ForeignKey(RewardsProgram)
  created_time = models.DateTimeField(auto_now_add=True, editable=False)
  updated_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)
  cred1 = models.CharField("Credential 1", max_length=255)
  cred2 = models.CharField("Credential 2", max_length=255, null=True)

class RewardsProgramAccountRevision(models.Model):
  account = models.ForeignKey(RewardsProgramAccount)
  pending = models.BooleanField(default=False)
  revision = models.PositiveIntegerField()
  created_time = models.DateTimeField(auto_now_add=True, editable=False)
  updated_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)

class RewardsProgramAccountRevisionEntry(models.Model):
  revision = models.ForeignKey(RewardsProgramAccountRevision)
  amount = models.PositiveIntegerField()
  expiration_date = models.DateField(null=True)
