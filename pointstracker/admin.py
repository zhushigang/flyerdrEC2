from django.contrib import admin
from pointstracker.models import *

admin.site.register(RewardsProgram)
admin.site.register(RewardsProgramAccount)

class RewardsProgramAccountRevisionEntryInline(admin.StackedInline):
  model = RewardsProgramAccountRevisionEntry

class RewardsProgramAccountRevisionAdmin(admin.ModelAdmin):
  inlines = [RewardsProgramAccountRevisionEntryInline]

admin.site.register(RewardsProgramAccountRevision, RewardsProgramAccountRevisionAdmin)
