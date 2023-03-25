import xmltodict
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Blog


# @login_required(login_url="/login/")
def keyword_searching(request):
    if request.method == "POST":
        keyword_searching = request.POST.get('keyword_searching')
        country_select = request.POST.get('country_select')
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic'}
        url = "https://google.com/complete/search?output=toolbar&gl=" + \
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
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def blog(request):
    blog = Blog.objects.all()
    context = {'segment': blog}
    html_template = loader.get_template('includes/blog.html')
    return HttpResponse(html_template.render(context,request))


def home(request):
   return render(request, 'includes/home.html')