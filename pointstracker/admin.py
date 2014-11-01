from django.contrib import admin
from pointstracker.models import *

class RewardsProgramAdmin(admin.ModelAdmin):
  list_display = ("__unicode__", "shortname", "displayname")

admin.site.register(RewardsProgram, RewardsProgramAdmin)

class RewardsProgramAccountAdmin(admin.ModelAdmin):
  list_display = ("__unicode__", "user", "rewards_program", "current_balance")

admin.site.register(RewardsProgramAccount, RewardsProgramAccountAdmin)

class RewardsProgramAccountRevisionEntryInline(admin.StackedInline):
  model = RewardsProgramAccountRevisionEntry

class RewardsProgramAccountRevisionAdmin(admin.ModelAdmin):
  inlines = [RewardsProgramAccountRevisionEntryInline]

admin.site.register(RewardsProgramAccountRevision, RewardsProgramAccountRevisionAdmin)
