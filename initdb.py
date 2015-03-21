#!/usr/bin/python

from p_admin.models import  EsthenosSettings,EsthenosUser
from p_organisation.models import EsthenosOrgApplicationHighMark,EsthenosOrgApplicationHighMarkRequest

user = EsthenosUser.create_user("admin","admin@esthenos.com","Admin312",True)
user.add_role("ADMIN")
user.first_name = "Admin"
user.last_name = ""
user.username = "Admin"
user.active = True
user.save()

if len(EsthenosSettings.objects.all()) ==1:
    EsthenosSettings.objects.all()[0].delete()

settings = EsthenosSettings()
print settings
settings.save()
#Added by Deepak
if len(EsthenosOrgApplicationHighMarkRequest.objects.all()) ==1:
    EsthenosOrgApplicationHighMarkRequest.objects.all()[0].delete()

settings = EsthenosOrgApplicationHighMarkRequest()
print settings
settings.save()
#Added By Deepak
if len(EsthenosOrgApplicationHighMark.objects.all()) ==1:
   EsthenosOrgApplicationHighMark.objects.all()[0].delete()

settings = EsthenosOrgApplicationHighMark()
print settings
settings.save()