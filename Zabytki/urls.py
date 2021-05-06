
from django.conf.urls import include, url
from Zabytki.views import HomePageView, parki_datasets, pomniki_datasets, unesco_datasets, zabytkiruchome_datasets
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path

from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^parki_data/$', parki_datasets, name='parki'),
    url(r'^pomniki_data/$', pomniki_datasets, name='pomniki'),
    url(r'^unesco_data/$', unesco_datasets, name='unesco'),
    url(r'^zabytkiruchome_data/$', zabytkiruchome_datasets, name='zabytkiruchome'),
    
    path('admin/', admin.site.urls),

    path('admin/login', auth_views.LoginView.as_view(), name='login'),
    path('admin/logout', auth_views.LogoutView.as_view(), name='logout'),
   
    

]
