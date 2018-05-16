import os
from django.core import management
from django.conf import settings
from django_cron import CronJobBase, Schedule


class Backup(CronJobBase):
    RUN_AT_TIMES = ['12:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'site_pet.Backup'

    def do(self):
        management.call_command('dbbackup') 
