# -*- coding: utf-8 -*-

import os
import xlrd
from .models import CustomUser
from django.contrib.auth.models import Permission


parki_shp = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'users.xls'))
loc = (parki_shp)
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
#sheet.cell_value(1, 1)
a=[]

for i in range(sheet.nrows):
   a.append(sheet.cell_value(i, 3))

users={(sheet.cell_value(i, 2)): [(sheet.cell_value(i, 4)),(sheet.cell_value(i,3)),(sheet.cell_value(i, 0)),(sheet.cell_value(i, 1))] for i in range(sheet.nrows)}

def run():
 
   permission1 = Permission.objects.get(name='Can add zabytki ruchome')
   permission2 = Permission.objects.get(name='Can add unesco')
   permission3 = Permission.objects.get(name='Can add pomniki historii')
   permission4 = Permission.objects.get(name='Can add parki kulturowe')
   permission5 = Permission.objects.get(name='Can delete zabytki ruchome')
   permission6 = Permission.objects.get(name='Can delete unesco')
   permission7 = Permission.objects.get(name='Can delete pomniki historii')
   permission8 = Permission.objects.get(name='Can delete parki kulturowe')
   permission9 = Permission.objects.get(name='Can change zabytki ruchome')
   permission10 = Permission.objects.get(name='Can change unesco')
   permission11 = Permission.objects.get(name='Can change pomniki historii')
   permission12 = Permission.objects.get(name='Can change parki kulturowe')
   
   #print(users)

   for user in users.keys():
      uzytkownik = CustomUser.objects.create_user(user, users[user][0], users[user][1])
      uzytkownik.Jednostka = users[user][2]
      uzytkownik.RDLP_Zak =users[user][3]
      uzytkownik.is_staff = True
      uzytkownik.user_permissions.set([permission1,permission2,permission3,permission4,permission5,permission6,permission7,permission8,permission9,permission10,permission11,permission12])
      uzytkownik.save()  
     
 