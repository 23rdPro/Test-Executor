import ntpath
import os

from fnmatch import filter as fn_filter

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


path1 = os.path.join(os.getcwd(), "executor/tests")
path2 = os.path.join(os.getcwd(), 'users/tests')

pattern = "test_*.py"

adjunct_path = [os.path.join(path2, f) for f in fn_filter(os.listdir(path2), pattern)]
paths = [os.path.join(path1, f) for f in fn_filter(os.listdir(path1), pattern)]

paths.extend(adjunct_path)


class Executor(models.Model):
    """
    Executor holds all crucial data related to a test executor in the database
    Fields:
        tester: user initiating a test
        environment_id: a unique integer field each test is executed in
        file: a m2m field object, each containing tests written in python, each executor can have more than one file
        created_at: a DateTimeField describing the time and date each Executor (test) was instantiated
        test_log: corresponding logs for each test
        test_status: definite verdict on each test run, passed or failed

    """
    ID_CHOICES = [(i, str(i)) for i in range(1, 101)]
    tester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    environment_id = models.IntegerField(choices=ID_CHOICES, unique=True)
    file = models.ManyToManyField("File")
    test_log = models.TextField(_('test log'), default='PENDING')
    test_status = models.CharField(_('test status'), max_length=8, default='PENDING')
    created_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return ', '.join(f.file for f in self.file.all())


class File(models.Model):
    """
    File identifies location where tests are found and stores the value in a character field named file

    """
    PATHS = [(ntpath.basename(paths[i]), ntpath.basename(paths[i])) for i in range(len(paths))]
    file = models.CharField(max_length=64, choices=PATHS, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.file
