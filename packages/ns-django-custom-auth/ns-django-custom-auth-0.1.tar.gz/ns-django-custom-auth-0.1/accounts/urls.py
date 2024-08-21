from .views import *
from django.urls import re_path
from django.contrib import admin


admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
    ## Authentication
    re_path(r'^signup/$', SignupApiView.as_view(), name='signup_api'),
    re_path(r'^login/$', LoginApiView.as_view(), name='login_api'),

]