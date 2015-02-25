from .models import *
import datetime
import hashlib
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def registerNewUser(userID,username,surname,email,password,usercell,request):
    user = Person(first_name=username, last_name=surname,email=email, identity=userID,password=password,cell_number=usercell,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user'}
    #print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    for i in user:
        if i.email == userEmail:
            userE = Person.objects.get(email=userEmail)
            
    if userEmail == "":
        return ""
    print "but i got here"
    if userE.password == userPassword:
        request.session['user']={'identity':userE.identity,'userRole':userE.userRole}
        data = {
            'name':userE.first_name,
            'surname':userE.last_name,
            'userID':userE.identity,
            'cellNo':userE.cell_number,
            'email':userE.email
        }
        return data
    else:
        return ""

def UploadAudio(Title,Description,Location,Date,request):
    file = request.FILES['audioFileUpload']
    user = Person.objects.get(identity=request.session['user']['identity'])
    
    hashed = hashlib.sha1()
    hashed.update(file.read())
    print hashed
    
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=hashed.hexdigest(),Person=user,audio=file)
    upload.save()
    data = {
            'name':user.first_name,
            'surname':user.last_name,
            'userID':user.identity,
            'cellNo':user.cell_number,
            'email':user.email
        }
    return data

def UploadVideo(Title,Description,Location,Date,request):
    file = request.FILES['videoFileUpload']
    user = Person.objects.get(identity=request.session['user']['identity'])
    
    hashed = hashlib.sha1()
    hashed.update(file.read())
    
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=hashed.hexdigest(),Person=user,video=file)
    upload.save()
    data = {
            'name':user.first_name,
            'surname':user.last_name,
            'userID':user.identity,
            'cellNo':user.cell_number,
            'email':user.email
        }
    return data

    
