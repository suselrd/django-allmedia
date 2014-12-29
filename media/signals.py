# coding=utf-8
from django.dispatch import Signal


pre_ajax_file_save = Signal(providing_args=['instance'])