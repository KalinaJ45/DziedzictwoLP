from django.contrib.gis import admin
from import_export import resources
from .models import ParkiKulturowe, UNESCO, PomnikiHistorii, ZabytkiRuchome
from leaflet.admin import LeafletGeoAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin, ExportActionModelAdmin, ImportExportActionModelAdmin
from import_export.formats import base_formats
from django.db import models
from django.contrib.gis.geos import WKTWriter
from django.contrib.gis.geos import GEOSGeometry
import shapefile
import geodaisy.converters as convert
from django.http import HttpResponse
from zipfile import ZipFile
import os
import shutil
import tempfile

#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'Jednostka','RDLP_Zak']
    fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Dane', {'fields': ('email','Jednostka','RDLP_Zak')}),
            ('Uprawnienia', {'fields': ('user_permissions',)}),
        )
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)





class UserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super(UserAdmin, self).get_fieldsets(request, obj))
        # update the `fieldsets` with your specific fields
        fieldsets.append(
            ('Personal info', {'fields': ('Jednostka')}))
        return fieldsets
    


class ParkiKulturoweResource(resources.ModelResource):

    class Meta:
        model = ParkiKulturowe
        fields = ('inspire_id', 'nazwa', 'informacje', 'kod_wojewdztwa', 'kod_powiatu', 'jednostka', 'RDLP_lub_zakład', 'uwagi')

class PomnikiHistoriiResource(resources.ModelResource):

    class Meta:
        model = PomnikiHistorii
        fields = ('inspire_id', 'nazwa', 'rodzaj_pomnika', 'dokładność_geometrii', 'rodzaj_dokumentu', ' data_utworzenia', 'kod_województwa', 'kod_powiatu', 'jednostka', 'RDLP_lub_zakład', 'uwagi')

class UNESCOResource(resources.ModelResource):

    class Meta:
        model = UNESCO
        fields = ('inspire_id', 'nazwa', ' rodzaj_dziedzictwa', 'dokładność_geometrii', 'rodzaj_dokumentu', ' data_utworzenia', 'kod_województwa', 'kod_powiatu', 'jednostka', 'RDLP_lub_zakład', 'uwagi')
 
class ZabytkiRuchomeResource(resources.ModelResource):

    class Meta:
        model = ZabytkiRuchome
        fields = ('nazwa', 'rodzaj_dokumentu', 'jednostka', 'RDLP_lub_zakład')



class ParkiKulturoweAdmin(LeafletGeoAdmin,ExportActionModelAdmin):
    km=None
    k=None
    list_display = ('inspire_id', 'nazwa')
    search_fields=['inspire_id', 'nazwa']
    resource_class = ParkiKulturoweResource	
    def get_export_formats(self):
        formats = (
          base_formats.XLS,
          base_formats.XLSX,
          base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]	
    def get_queryset(self, request):
        global km
        if request.user.is_superuser:
            km=ParkiKulturowe.objects.all() 
            return km  
        elif 'NADLEŚNICTWO' in request.user.Jednostka:
            km=ParkiKulturowe.objects.filter(jednostka__icontains=request.user.Jednostka)
            return km
        else:
            km=ParkiKulturowe.objects.filter(RDLP_lub_zakład__icontains=request.user.RDLP_Zak)
            return km	
    def coord(modeladmin, request, queryset):
        global km
        b=[]
        global k

        # some basename to save under
        basename = 'Parki_Kulturowe'
        #  create folder for this session
        temp_dir = tempfile.TemporaryDirectory()
        name=str(temp_dir.name)

        # export shp to this folder
        w = shapefile.Writer(f"{name}\{basename}\{basename}", encoding="utf8")
        all_fields=ParkiKulturowe._meta.get_fields()
        all_fields = [f.name for f in ParkiKulturowe._meta.fields]
        all_fields.remove('id')
        all_fields.remove('geometria')
        for f in all_fields:
            w.field(f, 'C', size=254)
            a=list(ParkiKulturowe.objects.values_list(f))
            b.append(a)
        
        for i in range (0,len(km)):
           w.record(b[0][i][0],b[1][i][0],b[2][i][0],b[3][i][0],b[4][i][0],b[5][i][0],b[6][i][0],b[7][i][0])
        for z in km:
            global k
            x=z.geometria
            coor=x.coords           
            k=[]
            h=[]
    
            for i in range (0,len(coor)):
                g=(list(coor[i][0]))
                h = [list(f) for f in g]
                k.append(h)

            w.poly(k)

        w.close()

        # create zip
        zipObj = ZipFile(f"{name}\{basename}.zip", 'w')
        
        #zip everything in the folder to the zip
        for file in os.listdir(str(f"{name}\{basename}")):
           zipObj.write(f"{name}\{basename}\{file}", file)   
        zipObj.close()
      
        # now we can server the zip file to the user
        filename = f'{name}\{basename}.zip'
    
        # check if file exists (just in case)
        try:
            fsock = open(filename, "rb")
        except:
            return HttpResponse(f"File '{basename}' Does Not Exist!",
            content_type='text/plain')
        #create response
        response = HttpResponse(fsock, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={basename}.zip'
        return response 

    coord.short_description = "Eksportuj jako Shapefile"
    actions=ImportExportActionModelAdmin.actions +['coord']
    #admin.site.add_action(coord)
  
    

class PomnikiHistoriiAdmin(LeafletGeoAdmin,ExportActionModelAdmin):
    pm=None
    v=None
    list_display = ('inspire_id', 'nazwa')
    search_fields=['inspire_id', 'nazwa']
    resource_class = PomnikiHistoriiResource
    def get_export_formats(self):
        formats = (
          base_formats.XLS,
          base_formats.XLSX,
          base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]
    def get_queryset(self, request):
        global pm
        if request.user.is_superuser:
            pm=PomnikiHistorii.objects.all()
            return pm    
        elif 'NADLEŚNICTWO' in request.user.Jednostka:
            pm=PomnikiHistorii.objects.filter(jednostka__icontains=request.user.Jednostka)
            return pm
        else:
            pm=PomnikiHistorii.objects.filter(RDLP_lub_zakład__icontains=request.user.RDLP_Zak)
            return pm

    def coord(modeladmin, request, queryset):
        global pm
        b=[]
        global v

        # some basename to save under
        basename = 'Pomniki_Historii'
        #  create folder for this session
        temp_dir = tempfile.TemporaryDirectory()
        name=str(temp_dir.name)

        # export shp to this folder
        w = shapefile.Writer(f"{name}\{basename}\{basename}", encoding="utf8")
        all_fields=PomnikiHistorii._meta.get_fields()
        all_fields = [f.name for f in PomnikiHistorii._meta.fields]
        all_fields.remove('id')
        all_fields.remove('geometria')
        for f in all_fields:
            w.field(f, 'C', size=254)
            a=list(PomnikiHistorii.objects.values_list(f))
            b.append(a)
        
        for i in range (0,len(pm)):
           w.record(b[0][i][0],b[1][i][0],b[2][i][0],b[3][i][0],b[4][i][0],b[5][i][0],b[6][i][0],b[7][i][0],b[8][i][0],b[9][i][0],b[10][i][0])
        for z in pm:
            global v
            x=z.geometria
            coor=x.coords                      
            v=[]
            h=[]
    
            for i in range (0,len(coor)):
                g=(list(coor[i][0]))
                h = [list(f) for f in g]
                v.append(h)

            w.poly(v)
           
        w.close()  

        # create zip
        zipObj = ZipFile(f"{name}\{basename}.zip", 'w')
        
        #zip everything in the folder to the zip
        for file in os.listdir(str(f"{name}\{basename}")):
           zipObj.write(f"{name}\{basename}\{file}", file)   
        zipObj.close()
      
        # now we can server the zip file to the user
        filename = f'{name}\{basename}.zip'
  
        # check if file exists (just in case)
        try:
            fsock = open(filename, "rb")
        except:
            return HttpResponse(f"File '{basename}' Does Not Exist!",
            content_type='text/plain')
        #create response
        response = HttpResponse(fsock, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={basename}.zip'
        return response 

    coord.short_description = "Eksportuj jako Shapefile"
    #admin.site.add_action(coord)
    actions=ImportExportActionModelAdmin.actions +['coord']

class UNESCOAdmin(LeafletGeoAdmin,ExportActionModelAdmin):
    um=None
    u=None
    list_display = ('inspire_id', 'nazwa')
    search_fields=['inspire_id', 'nazwa']
    resource_class = UNESCOResource
    def get_export_formats(self):
        formats = (
          base_formats.XLS,
          base_formats.XLSX,
          base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]
    def get_queryset(self, request):
        global um
        if request.user.is_superuser:
            um=UNESCO.objects.all()
            return um   
        elif 'NADLEŚNICTWO' in request.user.Jednostka:
            um=UNESCO.objects.filter(jednostka__icontains=request.user.Jednostka)
            return um
        else:
           um=UNESCO.objects.filter(RDLP_lub_zakład__icontains=request.user.RDLP_Zak)
           return um

    def coord(modeladmin, request, queryset):
        global um
        b=[]
        global u

       # some basename to save under
        basename = 'UNESCO'
        #  create folder for this session
        temp_dir = tempfile.TemporaryDirectory()
        name=str(temp_dir.name)

        # export shp to this folder
        w = shapefile.Writer(f"{name}\{basename}\{basename}", encoding="utf8")
        all_fields=UNESCO._meta.get_fields()
        all_fields = [f.name for f in UNESCO._meta.fields]
        all_fields.remove('id')
        all_fields.remove('geometria')
        for f in all_fields:
            w.field(f, 'C', size=254)
            a=list(UNESCO.objects.values_list(f))
            b.append(a)
        
        for i in range (0,len(um)):
           w.record(b[0][i][0],b[1][i][0],b[2][i][0],b[3][i][0],b[4][i][0],b[5][i][0],b[6][i][0],b[7][i][0],b[8][i][0],b[9][i][0])
        for u in um:
            global v
            x=u.geometria
            coor=x.coords
            print('lll')
            print(coor)
            v=[]
            h=[]
    
            for i in range (0,len(coor)):
                g=(list(coor[i][0]))
                h = [list(f) for f in g]
                v.append(h)

            w.poly(v)
           
        w.close()

        # create zip
        zipObj = ZipFile(f"{name}\{basename}.zip", 'w')
        
        #zip everything in the folder to the zip
        for file in os.listdir(str(f"{name}\{basename}")):
           zipObj.write(f"{name}\{basename}\{file}", file)   
        zipObj.close()
      
        # now we can server the zip file to the user
        filename = f'{name}\{basename}.zip'
        
        # check if file exists (just in case)
        try:
            fsock = open(filename, "rb")
        except:
            return HttpResponse(f"File '{basename}' Does Not Exist!",
            content_type='text/plain')
        #create response
        response = HttpResponse(fsock, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={basename}.zip'
        return response     

    coord.short_description = "Eksportuj jako Shapefile"
    #admin.site.add_action(coord)
    actions=ImportExportActionModelAdmin.actions +['coord']

class ZabytkiRuchomeAdmin(LeafletGeoAdmin,ExportActionModelAdmin):
    zm=None
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    list_display = ('nazwa',)
    search_fields=['nazwa']
    resource_class = ZabytkiRuchomeResource
    def get_export_formats(self):
        formats = (
          base_formats.XLS,
          base_formats.XLSX,
          base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]
    def get_queryset(self, request):
        global zm
        if request.user.is_superuser:
            zm=ZabytkiRuchome.objects.all()  
            return zm 
        elif 'NADLEŚNICTWO' in request.user.Jednostka:
            zm=ZabytkiRuchome.objects.filter(jednostka__icontains=request.user.Jednostka)
            return zm
        else:
            zm=ZabytkiRuchome.objects.filter(RDLP_lub_zakład__icontains=request.user.RDLP_Zak)
            return zm
    def coord(modeladmin, request, queryset):
        global zm
        b=[]

        # some basename to save under
        basename = 'Zabytki_Ruchome'
        #  create folder for this session
        temp_dir = tempfile.TemporaryDirectory()
        name=str(temp_dir.name)

        # export shp to this folder
        w = shapefile.Writer(f"{name}\{basename}\{basename}", encoding="utf8")
        all_fields=ZabytkiRuchome._meta.get_fields()
        all_fields = [f.name for f in ZabytkiRuchome._meta.fields]
        all_fields.remove('id')
        all_fields.remove('geometria')
        for f in all_fields:
            w.field(f, 'C', size=254)
            a=list(ZabytkiRuchome.objects.values_list(f))
            b.append(a)
        
        for i in range (0,len(zm)):
            w.record(b[0][i][0],b[1][i][0],b[2][i][0],b[3][i][0])
        for z in zm:
            
            x=z.geometria
            s=x.coords
            w.point(s[0][0], s[0][1])
            
        w.close()

        # create zip
        zipObj = ZipFile(f"{name}\{basename}.zip", 'w')
        
        #zip everything in the folder to the zip
        for file in os.listdir(str(f"{name}\{basename}")):
           zipObj.write(f"{name}\{basename}\{file}", file)   
        zipObj.close()
      
        # now we can server the zip file to the user
        filename = f'{name}\{basename}.zip'
        
        # check if file exists (just in case)
        try:
            fsock = open(filename, "rb")
        except:
            return HttpResponse(f"File '{basename}' Does Not Exist!",
            content_type='text/plain')
        #create response
        response = HttpResponse(fsock, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={basename}.zip'
        return response 
                
    coord.short_description = "Eksportuj jako Shapefile"
    #admin.site.add_action(coord)
    actions=ImportExportActionModelAdmin.actions +['coord']   
        


admin.site.register(ParkiKulturowe, ParkiKulturoweAdmin)
admin.site.register(PomnikiHistorii, PomnikiHistoriiAdmin)
admin.site.register(UNESCO, UNESCOAdmin)
admin.site.register(ZabytkiRuchome, ZabytkiRuchomeAdmin)

