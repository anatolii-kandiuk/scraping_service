from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()

    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    program_language = request.GET.get('program_language')
    page_obj = []
    context = {'city': city, 'program_language': program_language, 'form': form}
    if city or program_language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if program_language:
            _filter['program_language__slug'] = program_language

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj

    return render(request, 'scraping/list.html', context)