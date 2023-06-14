from django_cron import CronJobBase, Schedule
from datetime import date
from .models import BookInstance

class DeleteExpiredInstances(CronJobBase):
    RUN_EVERY_MINS = 24 * 60 # run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'book.delete_expired_instances'    # This is a unique code for your cronjob

    def do(self):
        BookInstance.objects.filter(due_back__lt=date.today()).delete()
        expired_instances = BookInstance.objects.filter(due_back__lt=date.today())
        for instance in expired_instances:
            instance.book.status = 'a'
            instance.book.save()