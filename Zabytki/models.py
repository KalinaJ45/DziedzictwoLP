from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class ParkiKulturowe(models.Model):

    inspire_id = models.CharField(max_length=50)
    nazwa = models.CharField(max_length=255)
    informacje = models.CharField(max_length=255)
    kod_województwa = models.CharField(max_length=2)
    kod_powiatu = models.CharField(max_length=4)
    nadleśnictwo = models.CharField(max_length=80)
    RDLP = models.CharField(max_length=80)
    uwagi = models.CharField(max_length=200)
    geometria = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.nazwa
    class Meta:
	    verbose_name_plural =" Parki kulturowe"

class UNESCO(models.Model):
    inspire_id = models.CharField(max_length=50)
    nazwa = models.CharField(max_length=100)
    rodzaj_dziedzictwa = models.CharField(max_length=254)
    dokładność_geometrii = models.CharField(max_length=254)
    rodzaj_dokumentu = models.CharField(max_length=100)
    data_utworzenia = models.CharField(max_length=4)
    kod_województwa = models.CharField(max_length=2)
    kod_powiatu = models.CharField(max_length=16)
    nadleśnictwo = models.CharField(max_length=80)
    RDLP = models.CharField(max_length=80)
    geometria = models.MultiPolygonField(srid=4326)
    
    def __str__(self):
        return self.nazwa
    class Meta:
	    verbose_name_plural =" Zabytki UNESCO"

class PomnikiHistorii(models.Model):
    inspire_id = models.CharField(max_length=50)
    nazwa = models.CharField(max_length=254)
    rodzaj_pomnika = models.CharField(max_length=254)
    dokładność_geometrii = models.CharField(max_length=254)
    rodzaj_dokumentu = models.CharField(max_length=100)
    data_utworzenia = models.CharField(max_length=10)
    kod_województwa = models.CharField(max_length=2)
    kod_powiatu = models.CharField(max_length=16)
    nadleśnictwo = models.CharField(max_length=80)
    RDLP = models.CharField(max_length=80)
    uwagi = models.CharField(max_length=200)
    geometria = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.nazwa
    
    class Meta:
	    verbose_name_plural =" Pomniki historii"

class ZabytkiRuchome(models.Model):
    nazwa = models.CharField(max_length=254)
    rodzaj_dokumentu = models.CharField(max_length=254)
    jednostka = models.CharField(max_length=254)
    RDLP_lub_zakład = models.CharField(max_length=254)
    geometria = models.MultiPointField(srid=4326)

    def __str__(self):
        return self.nazwa
    class Meta:
	    verbose_name_plural =" Zabytki ruchome"