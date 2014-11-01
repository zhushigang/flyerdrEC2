from django.contrib import admin
from pointstracker.models import *
from pointstracker import queue


class RewardsProgramAdmin(admin.ModelAdmin):
  list_display = ("__unicode__", "shortname", "displayname")

admin.site.register(RewardsProgram, RewardsProgramAdmin)

def refresh_balance(modeladmin, request, queryset):
  for account in queryset:
    queue.refresh_rewards_balance(account)

class RewardsProgramAccountAdmin(admin.ModelAdmin):
  list_display = ("__unicode__", "user", "rewards_program", "current_balance")
  actions=[refresh_balance]

admin.site.register(RewardsProgramAccount, RewardsProgramAccountAdmin)

class RewardsProgramAccountRevisionEntryInline(admin.StackedInline):
  model = RewardsProgramAccountRevisionEntry

class RewardsProgramAccountRevisionAdmin(admin.ModelAdmin):
  inlines = [RewardsProgramAccountRevisionEntryInline]

admin.site.register(RewardsProgramAccountRevision, RewardsProgramAccountRevisionAdmin)
