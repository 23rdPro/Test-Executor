# Test-Executor
Test Executor is a web application that enables authorized users to run automated tests over the internet. It is
developed with a python web framework, Django, and as such, its easily runnable on Debian systems with root access
on a virtual environment.
Python tests, depending on the actual nature usually takes a considerable amount of time to complete, which makes
running tests over an internet's request a time consuming task- we don't want this. Also, tests are configured to
return a value making python to exit with a code, so if the test failed, most likely our request that's already
taking longer than it should will fail- we do not want this neither. A solution would be to queue up tests away
from the original request, and ensure that the resulting log/status is associated with objects from the original
request. Celery appeared to be suitable for a task like this, and the doc states that: it’s a task queue with
focus on real-time processing, while also supporting task scheduling.
