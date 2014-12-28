from django.contrib.auth.models import User
from pointstracker import models
def get_balance(user):
	accounts = list(models.RewardsProgramAccount.objects.filter(user=user))
	json = dict()
	for account in accounts: 
		key = account.rewards_program.shortname
		
		revisions = list(models.RewardsProgramAccountRevision.objects.filter(account = account,pending=0))
		if len(revisions)>0:
			latest_revision = revisions[-1]
			entries = list(models.RewardsProgramAccountRevisionEntry.objects.filter(revision=latest_revision))
			value = entries[-1].amount
		else:
			value = "Account information not yet updated"
		
		json[key] = value
	
	programs = list(models.RewardsProgram.objects.all())
	shortnames = list()
	for program in programs:
		shortnames+=[program.shortname]
	for shortname in shortnames:
		if shortname not in json:
			json[shortname]="Please add your account"
	
	return json