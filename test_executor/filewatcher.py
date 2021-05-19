import os
import time
import re
from collections import OrderedDict

from watchdog.events import FileSystemEventHandler
from executor.models import Executor

name = 'output'


def read_test_log():
    res = {'test_file': [], 'test_log': [], 'test_status': []}
    lines = [line for line in reversed(open('output').readlines())][:82][::-1]
    keys = ['executor.tests.test_', 'users.tests.test_', 'ok', 'FAIL', 'AssertionError', 'self.assert', 'Ran']
    exclude = ['Running', 'Synchronizing', 'migrations', 'System', 'Preserving', 'Creating', 'Traceback', 'File',
               'Process', 'WorkerLostError', 'human_status']
    for ln in lines:
        if all([True if w not in exclude else False for w in ln.split()]) and 'OK (' not in ln:
            for k in keys:
                if (re.compile(r'(?<!\S)%s(?!\S)' % k, re.IGNORECASE).search(ln)) or \
                        (re.compile(r'(?<!\S)[(]%s(\w+)' % k, re.IGNORECASE).search(ln)) or \
                        (re.compile(r'(?<!\S)%s(\W+)' % k, re.IGNORECASE).search(ln)) or \
                        (re.compile(r'(?<!\S)%s(\w+)' % k, re.IGNORECASE).search(ln)):
                    try:
                        start = ln.index(']') + 1
                    except ValueError:
                        start = 0
                    log = ln[start:].strip()
                    if log not in res['test_log'] and log != 'ok':
                        res['test_log'].append(log)
                    if log == 'ok':
                        res['test_log'].append(log)

                    if (k == 'ok') and (ln.endswith(k)):
                        res['test_status'].append(True)
                    elif (k == 'FAIL') and (k in ln):
                        res['test_status'].append(False)

                    if k == 'executor.tests.test_' and k in ln:
                        start = ln.index(k) + len(k)
                        stop = ln.index('.', start)
                        file = ln[start:stop] + '.py'
                        if file not in res['test_file']:
                            res['test_file'].append(file)
                    elif k == 'users.tests.test_' and k in ln:
                        start = ln.index(k) + len(k)
                        stop = ln.index('.', start)
                        file = ln[start:stop] + '.py'
                        if file not in res['test_file']:
                            res['test_file'].append(file)

    res['test_status'] = 'PASSED' if all(res['test_status']) else 'FAILED'
    res['test_file'] = ['test_' + f for f in res['test_file']]
    # res['test_log'] = list(OrderedDict.fromkeys(res['test_log']))  # remove repetition, not suitable for my case
    return res


def update_test_object():
    result = read_test_log()
    if result['test_file'] and (', '.join(result['test_file']) == Executor.objects.last().__str__()) and \
            result['test_log'] and result['test_status']:
        Executor.objects.filter(id=Executor.objects.last().id).update(
            test_log='\n'.join(result['test_log']),
            test_status=result['test_status'],
        )


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(name):
            time.sleep(12)  # wait long enough for task to log all output
            update_test_object()
            try:
                time.sleep(1)
                os.remove('output')
            except FileNotFoundError:
                pass
