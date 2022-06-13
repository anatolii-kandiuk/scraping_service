import os, sys
import codecs

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from django.db import DatabaseError
from scraping.parsers import *
from scraping.models import Vacancy, City, ProgramLanguage, Error


parsers = (
    (work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
    (dou_ua, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (djinni, 'https://djinni.co/jobs/keyword-python/')
)

city = City.objects.filter(slug='kyiv').first()
program_language = ProgramLanguage.objects.filter(slug='python').first()
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, program_language=program_language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
