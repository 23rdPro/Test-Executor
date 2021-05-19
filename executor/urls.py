from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # path('', views.executors, name='executor_list'),
    # path('<int:pk>/', views.executor_detail, name='executor_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
