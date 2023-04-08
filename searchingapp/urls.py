from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('searching/', views.keyword_searching, name='searching'),
    path('blog/', views.blog, name='blog'),
    path('home/', views.home, name='home'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    # path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    # path('forgot/', views.forgot_password, name='forgot_password'),
    # path('reset/<str:reset_token>/', views.reset_password, name='reset_password'),
    path('signout/', views.logout_view, name='signout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

