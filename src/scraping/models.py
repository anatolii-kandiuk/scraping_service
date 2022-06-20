from django.db.models import (Model, CharField, SlugField,
                              URLField, TextField, DateField,
                              ForeignKey, CASCADE)
from jsonfield import JSONField   # Django 3.0


def default_urls():
    return {"work_ua": "", "dou_ua": "", "djinni": ""}


class City(Model):
    name = CharField(max_length=50, verbose_name='City name', unique=True)
    slug = SlugField(max_length=50, blank=True, unique=True)
    
    class Meta:
        verbose_name = 'City name'
        verbose_name_plural = 'Cities names'
    
    def __str__(self):
        return self.name


class ProgramLanguage(Model):
    name = CharField(max_length=50, verbose_name='Programming language', unique=True)
    slug = SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Programming language'
        verbose_name_plural = 'Programming languages'

    def __str__(self):
        return self.name


class Vacancy(Model):
    url = URLField(unique=True)
    title = CharField(max_length=1500, verbose_name='Title')
    company = CharField(max_length=1500, verbose_name='Company')
    description = TextField(verbose_name='Description')
    city = ForeignKey('City', on_delete=CASCADE, verbose_name='City')
    program_language = ForeignKey('ProgramLanguage', on_delete=CASCADE, verbose_name='Program language')
    timestamp = DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(Model):
    data = JSONField() # Django 3.0
    timestamp = DateField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)
    

class Url(Model):
    city = ForeignKey('City', on_delete=CASCADE, verbose_name='City')
    program_language = ForeignKey('ProgramLanguage', on_delete=CASCADE, verbose_name='Program language')
    url_data = JSONField(default=default_urls)
    
    class Meta:
        unique_together = ("city", "program_language")

