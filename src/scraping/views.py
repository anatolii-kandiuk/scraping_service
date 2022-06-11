from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    program_language = request.GET.get('program_language')
    qs = []

    if city or program_language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if program_language:
            _filter['program_language__slug'] = program_language

        qs = Vacancy.objects.filter(**_filter)

    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
