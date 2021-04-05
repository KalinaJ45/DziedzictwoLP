import os
from django.contrib.gis.utils import LayerMapping
from .models import ParkiKulturowe, UNESCO, PomnikiHistorii, ZabytkiRuchome


parkikulturowe_mapping = {
    'inspire_id': 'INSPIRE_ID',
    'nazwa': 'NAZWA',
    'informacje': 'INFORMACJE',
    'kod_województwa': 'KOD_WOJEWO',
    'kod_powiatu': 'KOD_POWIAT',
    'nadleśnictwo': 'NADL',
    'RDLP': 'RDLP',
    'uwagi': 'UWAGI',
    'geometria': 'MULTIPOLYGON',
}
parki_shp = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'data', 'Park_Kulturowy_area.shp'))

unesco_mapping = {
    'inspire_id': 'INSPIRE_ID',
    'nazwa': 'NAZWA',
    'rodzaj_dziedzictwa': 'RODZ_DZIE',
    'dokładność_geometrii': 'DOKL_GEOM',
    'rodzaj_dokumentu': 'RODZAJ_DOK',
    'data_utworzenia': 'DAT_UTW',
    'kod_województwa': 'KOD_WOJ',
    'kod_powiatu': 'KOD_POWIAT',
    'nadleśnictwo': 'NADL',
    'RDLP': 'RDLP',
    'geometria': 'MULTIPOLYGON',
}

UNESCO_shp = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'data', 'UNESCO_area.shp'))




pomnikihistorii_mapping = {
    'inspire_id': 'INSPIRE_ID',
    'nazwa': 'NAZWA',
    'rodzaj_pomnika': 'RODZ_PH',
    'dokładność_geometrii': 'DOKL_GEOM',
    'rodzaj_dokumentu': 'RODZAJ_DOK',
    'data_utworzenia': 'DAT_UTW',
    'kod_województwa': 'KOD_WOJ',
    'kod_powiatu': 'KOD_POWIAT',
    'nadleśnictwo': 'NADL',
    'RDLP': 'RDLP',
    'uwagi': 'UWAGI',
    'geometria': 'MULTIPOLYGON',
}

pomnikihistorii_shp = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'data', 'Pomniki_Historii_area.shp'))


zabytkiruchome_mapping = {
    'nazwa': 'NAZWA_ZABY',
    'rodzaj_dokumentu': 'DOKUMENT',
    'jednostka': 'JEDNOSTKA',
    'RDLP_lub_zakład': 'RDLP_ZAKL',
    'geometria': 'MULTIPOINT',
}

zabytkiruchome_shp = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'data', 'zab_ruch.shp'))


def run(verbose=True):
    lm = LayerMapping(ParkiKulturowe, parki_shp,
                      parkikulturowe_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

    lm2 = LayerMapping(UNESCO, UNESCO_shp,
                      unesco_mapping, transform=False, encoding='utf-8')
    lm2.save(strict=True, verbose=verbose)

    lm3 = LayerMapping(PomnikiHistorii, pomnikihistorii_shp,
                      pomnikihistorii_mapping, transform=False, encoding='utf-8')
    lm3.save(strict=True, verbose=verbose)

    lm4 = LayerMapping(ZabytkiRuchome, zabytkiruchome_shp,
                      zabytkiruchome_mapping, transform=False, encoding='utf-8')
    lm4.save(strict=True, verbose=verbose)
