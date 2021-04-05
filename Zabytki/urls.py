
from django.conf.urls import include, url
from Zabytki.views import HomePageView, parki_datasets, pomniki_datasets, unesco_datasets, zabytkiruchome_datasets


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^parki_data/$', parki_datasets, name='parki'),
    url(r'^pomniki_data/$', pomniki_datasets, name='pomniki'),
    url(r'^unesco_data/$', unesco_datasets, name='unesco'),
    url(r'^zabytkiruchome_data/$', zabytkiruchome_datasets, name='zabytkiruchome'),

]
