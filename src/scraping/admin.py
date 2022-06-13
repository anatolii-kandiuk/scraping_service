from django.contrib import admin
from .models import City, ProgramLanguage, Vacancy, Error


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProgramLanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(City, CityAdmin)
admin.site.register(ProgramLanguage, ProgramLanguageAdmin)
admin.site.register(Vacancy)
admin.site.register(Error)
