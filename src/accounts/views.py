from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('scraping:home')

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)

        return redirect('scraping:home')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('accounts:login')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        login(request, new_user)

        messages.success(request, 'Користувач доданий в систему')

        return redirect('scraping:home')

    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.program_language = data['program_language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Збережено')

                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={'city': user.city,
                     'program_language': user.program_language,
                     'send_email': user.send_email})

        return render(request, 'accounts/update.html', {'form': form,
                                                        'user_name': user.email})
    else:
        return redirect('accounts:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Користувача видалено')

    return redirect('accounts:login')
