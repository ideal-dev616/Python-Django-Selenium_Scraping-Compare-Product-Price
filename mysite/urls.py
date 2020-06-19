from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.loginpage, name='loginpage'),
    path('signup/', views.signuppage, name='signuppage'),
    path('logout/', views.logout, name='logout'),
    path('discounts/', views.discounts, name='discounts'),
    path('favourites/', views.favourites, name='favourites'),
    path('profile/', views.profile, name='profile'),
    url(r'^ajax/get_data_by_categ/$', views.get_data_by_categ, name='get_data_by_categ'),
    url(r'^ajax/add_favourite_list/$', views.add_favourite_list, name='add_favourite_list'),
    url(r'^ajax/comparison/$', views.comparison, name='comparison'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
