from django.contrib import admin
from .models import Person, caseAttribute, pdeAttribute, AuditLogCase, AuditLogPDE, personCase

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

class AuditLogCaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(AuditLogCase,AuditLogCaseAdmin)

class AuditLogPDEAdmin(admin.ModelAdmin):
    pass
admin.site.register(AuditLogPDE,AuditLogPDEAdmin)

class personCaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(personCase,personCaseAdmin)