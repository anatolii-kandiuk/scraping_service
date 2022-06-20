from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Vacancy, Error
from .forms import FindForm, ContactForm

import datetime as dt


def home_view(request):
    form = FindForm()
    contact_form = ContactForm()
    qs = Vacancy.objects.all()[:3]
    return render(request, 'scraping/home.html', {'form': form, 'contact_form': contact_form, 'object_list': qs})


def list_view(request):
    form = FindForm()
    contact_form = ContactForm()
    city = request.GET.get('city')
    program_language = request.GET.get('program_language')
    context = {'city': city, 'program_language': program_language, 'form': form, 'contact_form': contact_form}
    if city or program_language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if program_language:
            _filter['program_language__slug'] = program_language

        qs = Vacancy.objects.filter(**_filter)

        paginator = Paginator(qs, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['object_list'] = page_obj
        return render(request, 'scraping/home.html', context)
    else:
        messages.error(request, 'Нічого не знайдено')
        return redirect('scraping:home')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            program_language = data.get('program_language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email, 'program_language': program_language})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [
                    {'city': city, 'email': email, 'program_language': program_language}
                ]}
                Error(data=data).save()
            messages.success(request, 'Дані відправлені адміністрації.')
            return redirect('scraping:home')
        else:
            return redirect('scraping:home')
    else:
        return redirect('accounts:login')
