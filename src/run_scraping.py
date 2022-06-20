import asyncio
import os, sys
import datetime as dt

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from django.db import DatabaseError
from django.contrib.auth import get_user_model
from scraping.parsers import work_ua, dou_ua, djinni
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (work_ua, 'work_ua'),
    (dou_ua, 'dou_ua'),
    (djinni, 'djinni')
)
jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['program_language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['program_language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['program_language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


async def main(value):
    func, url, city, program_language = value
    job, err = await loop.run_in_executor(None, func, url, city, program_language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
tmp_tasks = [(func, data['url_data'][key], data['city'], data['program_language'])
             for data in url_list
             for func, key in parsers]

if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()

five_days_ago = dt.date.today() - dt.timedelta(5)
Vacancy.objects.filter(timestamp__lte=five_days_ago).delete()
