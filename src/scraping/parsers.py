import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work_ua', 'dou_ua', 'djinni')

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
]


def djinni(url, city=None, program_language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'

    if url:
        resp = requests.get(url, headers=headers[randint(0, 3)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('ul', attrs={'class': 'list-jobs'})

            if main_div:
                lst_li = main_div.find_all('li', attrs={'class': 'list-jobs__item'})

                for li in lst_li:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'list-jobs__description'})
                    content = cont.text
                    company = 'No name'
                    comp = li.find('div', attrs={'class': 'list-jobs__details__info'})

                    if comp:
                        company = comp.text

                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'program_language_id': program_language})
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def dou_ua(url, city=None, program_language=None):
    jobs = []
    errors = []

    if url:
        resp = requests.get(url, headers=headers[randint(0, 3)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')

            if main_div:
                lst_li = main_div.find_all('li', attrs={'class': 'l-vacancy'})

                for li in lst_li:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    content = cont.text
                    company = 'No name'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        company = a.text


                    jobs.append({'title': title.text,
                                 'url': href,
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'program_language_id': program_language})
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


def work_ua(url, city=None, program_language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 3)])

        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')

            if main_div:
                lst_div = main_div.find_all('div', attrs={'class': 'job-link'})

                for div in lst_div:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')

                    if logo:
                        company = logo['alt']

                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'program_language_id': program_language})
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://jobs.dou.ua/vacancies/?category=Python'
    jobs, errors = dou_ua(url)
    h = codecs.open('vacancies.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
