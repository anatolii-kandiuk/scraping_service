from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from scraping.models import City, ProgramLanguage, Vacancy
from .serializers import CitySerializer, ProgramLanguageSerializer, VacancySerializer

import datetime

period = datetime.date.today() - datetime.timedelta(1)


class DateFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        city_slug = request.query_params.get('city', None)
        pl_slug = request.query_params.get('pl', None)
        return queryset.filter(city__slug=city_slug, program_language__slug=pl_slug, timestamp__gte=period)


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProgramLanguageViewSet(ModelViewSet):
    queryset = ProgramLanguage.objects.all()
    serializer_class = ProgramLanguageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, DateFilterBackend)
    filterset_fields = ('city__slug', 'program_language__slug')
