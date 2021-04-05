from django.contrib.gis import admin
from .models import ParkiKulturowe, UNESCO, PomnikiHistorii, ZabytkiRuchome
from leaflet.admin import LeafletGeoAdmin


class ParkiKulturoweAdmin(LeafletGeoAdmin):
    list_display = ('inspire_id', 'nazwa')

class UNESCOAdmin(LeafletGeoAdmin):
    list_display = ('inspire_id', 'nazwa')

class PomnikiHistoriiAdmin(LeafletGeoAdmin):
    list_display = ('inspire_id', 'nazwa')

class ZabytkiRuchomeAdmin(LeafletGeoAdmin):
    list_display = ('nazwa',)

admin.site.register(ParkiKulturowe, ParkiKulturoweAdmin)
admin.site.register(PomnikiHistorii, PomnikiHistoriiAdmin)
admin.site.register(UNESCO, UNESCOAdmin)
admin.site.register(ZabytkiRuchome, ZabytkiRuchomeAdmin)

