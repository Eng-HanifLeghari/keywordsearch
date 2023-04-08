import xmltodict
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites import requests
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from .forms import LoginForm, SignUpForm, CustomPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Blog


# @login_required(login_url="login")
def keyword_searching(request):
    if request.method == "POST":
        keyword_searching = request.POST.get('keyword_searching')
        country_select = request.POST.get('country_select')
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic'}
        url = "https://api.keywordtool.io/v2/keyword_searching/volume/google" + \
              country_select + "&q=" + keyword_searching

        r = requests.get(url, headers=headers)
        coming = xmltodict.parse(r.text)
        suggestions = coming['toplevel']['CompleteSuggestion']
        keyword_list = []
        for suggestion in suggestions:
            for key, value in suggestion.items():
                if keyword_searching.lower() in value["@data"]:
                    keyword_list.append(value["@data"])
        context = {'segment': 'keyword_searching', 'keyword_list': keyword_list}

    else:
        context = {'segment': 'keyword_searching'}
    html_template = loader.get_template('apps/keyword_searching.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="register")
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            number = form.cleaned_data.get("number")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, email=email, number=number, password=raw_password)

            msg = 'User created successfully.'
            success = True

            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def logout_view(request):
    logout(request)
    return redirect('home')


# Forgot Password
# def password_reset(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             pass
#         else:
#             token = generate_unique_token()
#             user.password_reset_token = token
#             user.password_reset_token_created_at = timezone.now()
#             user.save()
#             send_password_reset_email(user.email, token)
#     return render(request, 'password_reset.html')


def password_reset_confirm(request, token):
    try:
        user = User.objects.get(password_reset_token=token)
    except User.DoesNotExist:
        pass
    else:
        if user.password_reset_token_created_at < timezone.now() - timezone.timedelta(hours=24):
            pass
        else:
            if request.method == 'POST':
                password = request.POST.get('password')
                user.set_password(password)
                user.password_reset_token = ''
                user.password_reset_token_created_at = None
                user.save()
    return render(request, 'password_reset_confirm.html')

# Reset password
from django.contrib import messages


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                from_email=request.POST.get('email'),
                email_template_name='password_reset_email.html',
                subject_template_name='password_reset_subject.txt',
            )
            messages.success(request, 'An email has been sent to you with instructions on how to reset your password.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})


# Change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def blog(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    html_template = loader.get_template('includes/blog.html')
    return HttpResponse(html_template.render(context, request))


def home(request):
   return render(request, 'includes/home.html')