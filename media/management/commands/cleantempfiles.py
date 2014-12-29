# coding=utf-8
from django.core.management.base import NoArgsCommand
from ...tasks import clean_temp_files


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        clean_temp_files()
