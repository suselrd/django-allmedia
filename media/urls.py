# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from .views import HandleAjaxFileUploadedView

urlpatterns = patterns('',
    # BASICS

    url(
        r'^upload/file/$',
        login_required(HandleAjaxFileUploadedView.as_view()),
        name="upload_file"
    ),

)
