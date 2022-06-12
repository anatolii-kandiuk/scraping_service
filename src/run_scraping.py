from scraping.parsers import *
import codecs

parsers = ((work_ua, 'https://www.work.ua/jobs-kyiv-python/'),
           (dou_ua, 'https://jobs.dou.ua/vacancies/?category=Python'),
           djinni, 'https://djinni.co/jobs/keyword-python/')

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('vacancies.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()