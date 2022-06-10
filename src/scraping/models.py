from django.db.models import (Model, CharField, SlugField, URLField, TextField, DateField,
                              ForeignKey, CASCADE, )


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
    title = CharField(max_length=250, verbose_name='Title')
    company = CharField(max_length=250, verbose_name='Company')
    description = TextField(verbose_name='Description')
    city = ForeignKey('City', on_delete=CASCADE, verbose_name='')
    program_language = ForeignKey('ProgramLanguage', on_delete=CASCADE, verbose_name='Program language')
    timestamp = DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return self.title
