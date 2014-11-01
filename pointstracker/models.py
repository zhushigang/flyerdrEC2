from django.db import models
from django.contrib.auth.models import User

import datetime

class RewardsProgram(models.Model):
  shortname = models.CharField(max_length=32, unique=True)
  displayname = models.CharField(max_length=255)
  created_time = models.DateTimeField(auto_now_add=True, editable=False)
  updated_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)

  def __unicode__(self):
    return self.displayname

class RewardsProgramAccount(models.Model):
  user = models.ForeignKey(User)
  rewards_program = models.ForeignKey(RewardsProgram, related_name="accounts", related_query_name="account")
  created_time = models.DateTimeField(auto_now_add=True, editable=False)
  updated_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)
  cred1 = models.CharField("Credential 1", max_length=255)
  cred2 = models.CharField("Credential 2", max_length=255, null=True)

  def __unicode__(self):
    return "{0} for {1}".format(self.rewards_program, self.user)

  def current_balance(self):
    try:
      return self.revisions.order_by('-updated_time')[0].get_current_balance()
    except IndexError:
      return None

class RewardsProgramAccountRevision(models.Model):
  account = models.ForeignKey(RewardsProgramAccount, related_name="revisions", related_query_name="revision")
  pending = models.BooleanField(default=False)
  created_time = models.DateTimeField(auto_now_add=True, editable=False)
  updated_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)

  def __unicode__(self):
    return "{0} rev {1}".format(self.account, self.id)

  def get_current_balance(self):
    if self.pending: return None
    now = datetime.date.today()
    return sum(x.amount for x in self.entries.all() if x.expiration_date is None or x.expiration_date > now)

class RewardsProgramAccountRevisionEntry(models.Model):
  revision = models.ForeignKey(RewardsProgramAccountRevision, related_name="entries", related_query_name="entry")
  amount = models.PositiveIntegerField()
  expiration_date = models.DateField(null=True)

  def __unicode__(self):
    s = "{0} points".format(self.amount)
    if self.expiration_date != None:
      s += " expires {0}".format(self.expiration_date)
    return s
