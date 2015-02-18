from django.contrib import admin
from .models import Person, caseAttribute, pdeAttribute

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(Person,PersonAdmin)

class caseAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(caseAttribute,caseAttributeAdmin)

class pdeAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(pdeAttribute,pdeAttributeAdmin)
