from .models import *
import datetime
import hashlib
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def registerNewUser(userID,username,surname,email,password,usercell,request):
    user = Person(first_name=username, last_name=surname,email=email, identity=userID,password=password,cell_number=usercell,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user', 'first_name': username, 'last_name':surname}
    #print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    found = False
    for i in user:
        if i.email == userEmail:
            userE = Person.objects.get(email=userEmail)
            found = True
        
            
    if found == False:
        return ""
    
    print "but i got here"
    if userE.password == userPassword:
        request.session['user']={'identity':userE.identity,'userRole':userE.userRole, 'first_name':userE.first_name, 'last_name':userE.last_name}
        if userE.userRole == 'user':
            data = {
                'name':userE.first_name,
                'surname':userE.last_name,
                'userID':userE.identity,
                'cellNo':userE.cell_number,
                'email':userE.email,
                'userRole':userE.userRole
            }
        else:
            pde = pdeAttribute.objects.filter()
            images = []
            audio = []
            video = []
            for value in pde:
                if value.photo:
                    name = value.photo.name
                    sts = name.split('/')
                    images.append({'title': value.title, 'data': sts[1],'id':value.id})
                elif value.audio:
                    name = value.audio.name
                    sts = name.split('/')
                    audio.append({'title': value.title, 'data': sts[1],'id':value.id})
                elif value.video:
                    name = value.video.name
                    sts = name.split('/')
                    video.append({'title': value.title, 'data': sts[1],'id':value.id})
            
            data = {
                'name':userE.first_name,
                'surname':userE.last_name,
                'userID':userE.identity,
                'cellNo':userE.cell_number,
                'email':userE.email,
                'userRole':userE.userRole,
                'images':images,
                'audio':audio,
                'video':video,
                'date':str(datetime.date.today())
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

def uploadImage(request, title_, description_, location_, date_, userID_):
    image = request.FILES['imageFileUpload']
    
    per = Person.objects.get(identity = userID_)
    
    pde = pdeAttribute(title=title_, description=description_, location=location_, date=datetime.datetime.now(), Person=per, photo=image)
    pde.save()
    
    if per is not None:
        data = {
            'name':per.first_name,
            'surname':per.last_name,
            'userID':per.identity,
            'cellNo':per.cell_number,
            'email':per.email
        }
        return data
    else:
        return ""
    
def viewProfile(userID):
    data = []
    
    per = Person.objects.get(identity = userID) 
    allUploads = pdeAttribute.objects.filter(Person = per)
    
    photoUploads = []
    videoUploads = []
    audioUploads = []
    
    for upload in allUploads:
        if upload.video:
            name = upload.video.name
            sts = name.split('/')
            print sts
            list = []
            list.append(upload.title)
            list.append(sts[1])
            videoUploads.append(list)
            
        elif upload.photo:
            name = upload.photo.name
            sts = name.split('/')
            list = []
            list.append(upload.title)
            list.append(sts[1])
            photoUploads.append(list)
        
        
        
        elif upload.audio:
            name = upload.audio.name
            sts = name.split('/')
            list = []
            list.append(upload.title)
            list.append(sts[1])
            audioUploads.append(list)
            

    
    data.append(per.first_name)
    data.append(per.last_name)
    data.append(per.identity)
    data.append(per.cell_number)
    data.append(per.email)
    data.append(photoUploads)
    data.append(videoUploads)
    data.append(audioUploads)
    
    return data

def viewImage(request,image):
    pde = pdeAttribute.objects.get(id=image)
    userE = Person.objects.get(identity=request.session['user']['identity'])
    case = None
    if pde.caseAttribute:
        case = pde.caseAttribute.caseNumber
    
    Iname = pde.photo.name
    sts = Iname.split('/')
    
    caseObj = caseAttribute.objects.all()
    list = []
    for i in caseObj:
        list1 = []
        list1.append(i.caseNumber)
        list1.append(i.id)
        list.append(list1)
    
    data = {
        'name':userE.first_name,
        'surname':userE.last_name,
        'title':pde.title,
        'description':pde.description,
        'location':pde.location,
        'date':str(pde.date),
        'caseNumber':case,
        'imageName':sts[1],
        'arrayCases':list
    }
    
    return data
    

def leaHomePage(request):
    userE = Person.objects.get(identity=request.session['user']['identity'])
    pde = pdeAttribute.objects.filter()
    images = []
    audio = []
    video = []
    for value in pde:
        if value.photo:
            name = value.photo.name
            sts = name.split('/')
            images.append({'title': value.title, 'data': sts[1],'id':value.id})
        elif value.audio:
            name = value.audio.name
            sts = name.split('/')
            audio.append({'title': value.title, 'data': sts[1],'id':value.id})
        elif value.video:
            name = value.video.name
            sts = name.split('/')
            video.append({'title': value.title, 'data': sts[1],'id':value.id})
    
            
    data = {
                'name':userE.first_name,
                'surname':userE.last_name,
                'images':images,
                'audio':audio,
                'video':video,
                'date':str(datetime.date.today())
        }
    return data

def assignCase(pdeID,caseID):
    pde = pdeAttribute.objects.get(id=pdeID)
    case = caseAttribute.objects.get(id=caseID)
    
    pde.caseAttribute = case
    pde.save()
    print "+++++++++++++++++++++++++++++++++++++++++++"
    print str(pde.caseAttribute.caseNumber)
    return True;

def viewVideo(request,video):
    pde = pdeAttribute.objects.get(id=video)
    userE = Person.objects.get(identity=request.session['user']['identity'])
    case = None
    if pde.caseAttribute:
        case = pde.caseAttribute.caseNumber
    
    Iname = pde.video.name
    sts = Iname.split('/')
    
    caseObj = caseAttribute.objects.all()
    list = []
    for i in caseObj:
        list1 = []
        list1.append(i.caseNumber)
        list1.append(i.id)
        list.append(list1)
    
    data = {
        'name':userE.first_name,
        'surname':userE.last_name,
        'title':pde.title,
        'description':pde.description,
        'location':pde.location,
        'date':str(pde.date),
        'caseNumber':case,
        'videoName':sts[1],
        'arrayCases':list
    }
    
    return data

def viewAudio(request,audio):
    pde = pdeAttribute.objects.get(id=audio)
    userE = Person.objects.get(identity=request.session['user']['identity'])
    case = None
    if pde.caseAttribute:
        case = pde.caseAttribute.caseNumber
    
    Iname = pde.audio.name
    sts = Iname.split('/')
    
    caseObj = caseAttribute.objects.all()
    list = []
    for i in caseObj:
        list1 = []
        list1.append(i.caseNumber)
        list1.append(i.id)
        list.append(list1)
    
    data = {
        'name':userE.first_name,
        'surname':userE.last_name,
        'title':pde.title,
        'description':pde.description,
        'location':pde.location,
        'date':str(pde.date),
        'caseNumber':case,
        'audioName':sts[1],
        'arrayCases':list
    }
    
    return data


    
