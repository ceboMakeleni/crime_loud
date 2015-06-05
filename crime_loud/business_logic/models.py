from django.db import models
from simplecrypt import encrypt, decrypt
import binascii

#Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    id = models.CharField(max_length=13, primary_key = True)
    email = models.CharField(max_length=1000)
    password=models.CharField(max_length=1000)
    userRole=models.CharField(max_length=4)
    
    def __unicode__(self):
        return decrypt('pde%attr@137',binascii.a2b_base64(self.first_name))

class caseAttribute(models.Model):
    caseName = models.CharField(max_length=30)
    caseNumber=models.CharField(max_length=20)
    person = models.ForeignKey(Person)
    
    def __unicode__(self):
      return self.caseName + " "+self.caseNumber

class personCase(models.Model):
    person = models.ForeignKey(Person)
    case = models.ForeignKey(caseAttribute)
    Type = models.CharField(max_length=4,null=True )
    
    def __unicode__(self):
      return self.case.caseNumber

class pdeAttribute(models.Model):
    title = models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    location=models.CharField(max_length=40)
    date=models.DateTimeField()
    digitalData=models.CharField(max_length=1000,null=True)
    caseAttribute=models.ForeignKey(caseAttribute, null=True)
    Person = models.ForeignKey(Person) #Person who uploaded
    photo = models.FileField(upload_to='photo',null=True)
    video = models.FileField(upload_to='video',null=True)
    audio = models.FileField(upload_to='audio',null=True)
    
    def __unicode__(self):
        return self.title

class leaDigitalEvidence(models.Model):
    title = models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    location=models.CharField(max_length=40)
    date=models.DateTimeField()
    digitalData=models.CharField(max_length=1000,null=True)
    caseAttribute=models.ForeignKey(caseAttribute, null=True)
    Person = models.ForeignKey(Person) #Person who uploaded
    photo = models.FileField(upload_to='photo',null=True)
    video = models.FileField(upload_to='video',null=True)
    audio = models.FileField(upload_to='audio',null=True)
    
    def __unicode__(self):
        return self.title
    
class AuditLogCase(models.Model):
    person_id = models.ForeignKey(Person)
    action = models.CharField(max_length=20)
    date = models.DateTimeField()
    old_value=models.CharField(max_length=100,null=True)
    new_value=models.CharField(max_length=100,null=True)
    
class AuditLogPDE(models.Model):
    person_id = models.ForeignKey(Person)
    action=models.CharField(max_length=20)
    date = models.DateTimeField()
    pde_title=models.CharField(max_length=100)
    pde_date = models.DateTimeField()
    pde_location = models.CharField(max_length=40)

class AuditLogDigitalEvidence(models.Model):
    person_id = models.ForeignKey(Person)
    action=models.CharField(max_length=20)
    date = models.DateTimeField()
    pde_title=models.CharField(max_length=100)
    pde_date = models.DateTimeField()
    pde_location = models.CharField(max_length=40)

