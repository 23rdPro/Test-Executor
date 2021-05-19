from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import permissions, viewsets, status
from django.db import transaction
from rest_framework.response import Response

from . import tasks
from .forms import ExecutorForm
from .models import Executor, File
# from .permissions import AdminAuthenticationPermission
from .serializers import FileSerializer, ExecutorSerializer, TaskSerializer


@login_required
def execute_test(request):  # execute_test handles test execution view and task scheduling
    tester = request.user
    if request.method == 'POST':
        form = ExecutorForm(tester, request.POST or None)
        if form.is_valid():
            file = form.cleaned_data.get('file')
            files = [str(f)[:-3] for f in file]  # index to avoid file name with `.py`-> test sees it as an attribute
            form.save()
            transaction.on_commit(lambda: tasks.execute_test_from.delay(files))
            return redirect('result')
        else:
            messages.error(request, 'Please revise provided information', extra_tags='alert')
            return render(request, "executor.html", {'form': form})
    else:
        form = ExecutorForm(tester)
    return render(request, "executor.html", {'form': form})


def get_result(request):  # a JsonResponse view, responsible for sending executor values as dict for frontend scripting
    if request.is_ajax and request.method == 'GET':
        executor = Executor.objects.last()  # most recent executor obj
        data = TaskSerializer(executor).data
        # print(data)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({}, status=400)


# to upload test file
# @login_required
# def upload_test_file(request):
#     if request.method == 'POST':
#         form = UploadTestFileForm(request.POST or None, request.FILES)
#         if form.is_valid():
#             file_upload(request.FILES['file'])
#             return HttpResponse('Upload Successful')
#             # return HttpResponseRedirect('/upload-success/')
#     else:
#         form = UploadTestFileForm()
#     template_name = 'upload.html'
#     return render(request, template_name, {'form': form})


@login_required
def test_executor_result_view(request):
    executors = list(Executor.objects.all())[:-1]  # all objects bar the just submitted one, [] if none
    template_name = "result.html"
    context = {"executors": executors}
    return render(request, template_name, context)


#####################################################################################
# REST Service
#####################################################################################

class FileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExecutorViewSet(viewsets.ModelViewSet):
    queryset = Executor.objects.all().order_by('id')
    serializer_class = ExecutorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # the create method provides a way to perform an on_commit transaction so as to have access to test executor
    def create(self, request, *args, **kwargs):
        serializer = ExecutorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            files = [item['file'][:-3] for item in serializer.data['file']]
            transaction.on_commit(lambda: tasks.execute_test_from.delay(files))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
