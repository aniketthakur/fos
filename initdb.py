#!/usr/bin/python

from p_admin.models import  EsthenosSettings,EsthenosUser

#user = EsthenosUser.create_user("admin","admin@esthenos.com",True)
#user.add_role("ADMIN")
#user.is_active = True
#user.save()

if len(EsthenosSettings.objects.all()) ==1:
    EsthenosSettings.objects.all()[0].delete()

settings = EsthenosSettings()
print settings
settings.save()

