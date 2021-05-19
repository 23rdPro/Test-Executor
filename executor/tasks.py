import os
from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.management import call_command
from .models import path1, path2

logger = get_task_logger(__name__)


@shared_task
def execute_test_from(files):
    if isinstance(files, list):
        dir1 = ['executor.tests.' + file for file in files if file + '.py' in os.listdir(path1)]
        dir2 = ['users.tests.' + file for file in files if file + '.py' in os.listdir(path2)]
        fs = dir1 + dir2

        if len(fs) == 1:
            call_command('test', fs[0], verbosity=3)
        elif len(fs) == 2:
            call_command('test', fs[0], fs[1], verbosity=3)
        elif len(fs) == 3:
            call_command('test', fs[0], fs[1], fs[2], verbosity=3)
        elif len(fs) == 4:
            call_command('test', fs[0], fs[1], fs[2], fs[3], verbosity=3)
        elif len(fs) == 5:
            call_command('test', fs[0], fs[1], fs[2], fs[3], fs[4], verbosity=3)
        elif len(fs) == 6:
            call_command('test', fs[0], fs[1], fs[2], fs[3], fs[4], fs[5], verbosity=3)
        elif len(fs) == 7:
            call_command('test', fs[0], fs[1], fs[2], fs[3], fs[4], fs[5], fs[6], verbosity=3)
