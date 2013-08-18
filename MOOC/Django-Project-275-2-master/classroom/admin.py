from django.contrib import admin
from classroom.models import MOOC_User

class MOOCAdmin(admin.ModelAdmin):
      list_display    = ['primaryURL', 'secondaryURL']
admin.site.register(MOOC_User, MOOCAdmin)

