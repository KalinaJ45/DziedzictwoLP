from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.serializers import serialize
from Zabytki.models import ParkiKulturowe, PomnikiHistorii, UNESCO, ZabytkiRuchome
from django.http import HttpResponse


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'index.html'


def parki_datasets(request):
    parki = serialize('geojson', ParkiKulturowe.objects.all())
    return HttpResponse(parki, content_type='json')

def pomniki_datasets(request):
    pomniki = serialize('geojson', PomnikiHistorii.objects.all())
    return HttpResponse(pomniki, content_type='json')

def unesco_datasets(request):
    unesco = serialize('geojson', UNESCO.objects.all())
    return HttpResponse(unesco, content_type='json')

def zabytkiruchome_datasets(request):
    zabytkiruchome = serialize('geojson', ZabytkiRuchome.objects.all())
    return HttpResponse(zabytkiruchome, content_type='json')

