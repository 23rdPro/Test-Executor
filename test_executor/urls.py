from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from executor.views import execute_test, get_result, test_executor_result_view
from users import views
from executor import views as api_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'files', api_views.FileViewSet, basename='file')
router.register(r'executors', api_views.ExecutorViewSet, basename='executor')

urlpatterns = [
    # admin routes
    path('admin/', admin.site.urls),

    # api routes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # app routes
    path('', execute_test, name='home'),
    path('response/', get_result, name='response'),  # json response
    path('result/', test_executor_result_view, name='result'),
    # to upload test files
    # path('upload/', upload_test_file, name='upload'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
