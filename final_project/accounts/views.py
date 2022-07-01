from django import forms
from django.contrib import messages

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from movies.models import Movie
from star_ratings.models import UserRating

from .forms import SignupForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .tokens import account_activation_token


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(email=form_data['email'], password=form_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, 'електронна адреса або пароль неправильні')
                render(request, 'accounts/account/login.html')
    else:
        form = LoginForm()
    return render(request, 'accounts/account/login.html', {'form': form})


def signup(request):
    """User signup with confirmation email."""

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активуйте свій обліковий запис.'
            # send confirmation email
            message = render_to_string('accounts/account/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Підтвердьте свою електронну адресу, щоб завершити реєстрацію')
    else:
        form = SignupForm()
    return render(request, 'accounts/account/signup.html', {'form': form})


def activate(request, uidb64, token):
    """Signup confirmation."""

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.google_auth = False
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('Дякуємо за підтвердження електронної пошти. Тепер ви можете увійти в обліковий запис.')
    else:
        return HttpResponse('Посилання для активації недійсне!')


@login_required
def profile(request):
    user = request.user
    user_profile = request.user.profile
    return render(request, 'accounts/account/profile.html', {'user': user, 'user_profile': user_profile})


@login_required
def watchlist(request):
    movies_all = request.user.profile.watchlist.all()
    paginator = Paginator(movies_all, 8)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)
    return render(request, 'accounts/account/watchlist.html', {'movies': movies})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профіль успішно оновлено')
            return redirect(to='/account/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'accounts/account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """Password reset with confirmation email."""

    template_name = 'accounts/password/password_reset.html'
    email_template_name = 'accounts/password/password_reset_email.html'
    subject_template_name = 'accounts/password//password_reset_subject.txt'
    success_message = "Ми надіслали вам інструкції щодо встановлення пароля " \
                       "якщо існує обліковий запис із введеною вами електронною поштою. Ви отримаєте їх найближчим часом." \
                       " Якщо ви не отримали електронного листа, " \
                       "будь ласка, переконайтеся, що ви ввели адресу, за якою ви зареєструвалися, і перевірте папку зі спамом."
    success_url = '/account/login'


@login_required
def change_password(request):
    """Password change."""

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # omit old password confirmation if user is authenticated with google account
        if request.user.profile.google_auth:
            form.fields.pop('old_password')
        if form.is_valid():
            request.user.profile.google_auth = False
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Ваш пароль успішно оновлено!')
            return redirect(to='/account/')
    else:
        form = PasswordChangeForm(request.user)
        for field in form.fields:
            form.fields[field].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        # omit old password form field if user is authenticated with google account
        if request.user.profile.google_auth:
            form.fields['old_password'].disabled = True
            form.fields.pop('old_password')

    return render(request, 'accounts/password/change_password.html', {
        'form': form
    })


@login_required
def ratings(request):
    """Get and show user ratings."""

    movies_all = []
    for rate in UserRating.objects.filter(user=request.user):
        movie = get_object_or_404(Movie, id=rate.rating.object_id)
        movies_all.append(movie)

    paginator = Paginator(movies_all, 8)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)
    return render(request, 'accounts/account/ratings.html', {'movies': movies})
