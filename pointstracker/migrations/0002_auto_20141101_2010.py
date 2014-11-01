# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pointstracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rewardsprogramaccountrevision',
            name='revision',
        ),
        migrations.AlterField(
            model_name='rewardsprogramaccount',
            name='rewards_program',
            field=models.ForeignKey(related_query_name=b'account', related_name='accounts', to='pointstracker.RewardsProgram'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rewardsprogramaccountrevision',
            name='account',
            field=models.ForeignKey(related_query_name=b'revision', related_name='revisions', to='pointstracker.RewardsProgramAccount'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rewardsprogramaccountrevisionentry',
            name='revision',
            field=models.ForeignKey(related_query_name=b'entry', related_name='entries', to='pointstracker.RewardsProgramAccountRevision'),
            preserve_default=True,
        ),
    ]
