from django.urls import path, re_path
from . import views
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('searching/', views.keyword_searching, name='searching'),
    path('blog/', views.blog, name='blog'),
    path('home/', views.home, name='home'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]