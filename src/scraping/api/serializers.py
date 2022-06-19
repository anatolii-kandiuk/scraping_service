from rest_framework.serializers import ModelSerializer
from scraping.models import City, ProgramLanguage, Vacancy


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'slug')


class ProgramLanguageSerializer(ModelSerializer):
    class Meta:
        model = ProgramLanguage
        fields = ('name', 'slug')


class VacancySerializer(ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'
        