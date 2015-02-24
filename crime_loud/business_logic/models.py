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

class caseAttribute(models.Model):
    caseName = models.CharField(max_length=30)
    caseNumber=models.CharField(max_length=20)
    person = models.ForeignKey(Person)

class pdeAttribute(models.Model):
    title = models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    location=models.CharField(max_length=40)
    date=models.DateTimeField()
    digitalData=models.CharField(max_length=30, null=True)# For the hash of the image
    caseAttribute=models.ForeignKey(caseAttribute, null=True)
    Person = models.ForeignKey(Person)
    photo = models.FileField(upload_to='photo',null=True)
    video = models.FileField(upload_to='video',null=True)
    audio = models.FileField(upload_to='audio',null=True)