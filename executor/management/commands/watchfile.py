import os
import time

from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from test_executor.filewatcher import FileHandler

path = os.path.join(os.getcwd())


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        event_handler = FileHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)  #
        observer.start()
        try:
            while True:
                time.sleep(1)  #
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
