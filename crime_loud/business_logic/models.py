from django.db import models

#Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    identity = models.CharField(max_length=13)
    cell_number = models.CharField(max_length=10,default="")
    email = models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    userRole=models.CharField(max_length=4)

#class personCase(models.Model):
#    person = models.ForeignKey(Person)
#    case = models.ForeignKey(caseAttribute)

class caseAttribute(models.Model):
    caseName = models.CharField(max_length=30)
    caseNumber=models.CharField(max_length=20)
    person = models.ForeignKey(Person)

class pdeAttribute(models.Model):
    title = models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    location=models.CharField(max_length=40)
    date=models.DateTimeField()
    digitalData=models.CharField(max_length=50,null=True)
    caseAttribute=models.ForeignKey(caseAttribute, null=True)
    Person = models.ForeignKey(Person) #Person who uploaded
    photo = models.FileField(upload_to='photo',null=True)
    video = models.FileField(upload_to='video',null=True)
    audio = models.FileField(upload_to='audio',null=True)
    
#class AuditLogCase(models.Model):
#    person_id = models.ForeignKey(Person)
#    action = models.CharField(max_length=20)
#    old_value=models.CharField(max_length=100,null=True)
#    new_value=models.CharField(max_length=100,null=True)
#    
#class AuditLogPDE(models.Model):
#    person_id = models.ForeignKey(person)
#    action=models.CharField(max_length=20)
#    pde_name=models.CharField(max_length=100)
    

    