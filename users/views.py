from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import viewsets, permissions

from executor.permissions import AdminAuthenticationPermission
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User
from users.serializers import UserSerializer


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Success! Welcome %s' % username, extra_tags='alert')
            return redirect('home')
        else:
            messages.warning(request, 'Please revise provided information', extra_tags='alert')
            return render(request, 'signup.html', {'form': form, })
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form, })


# REST
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
