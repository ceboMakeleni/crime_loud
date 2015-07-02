from .models import *
import datetime
import hashlib
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from simplecrypt import encrypt, decrypt
import binascii

def registerNewUser(userID,username,surname,email,password,request):
    text_name = binascii.b2a_base64(encrypt('pde%attr@137',username))
    text_surname = binascii.b2a_base64(encrypt('pde%attr@137',surname))
    text_password = binascii.b2a_base64(encrypt('pde%attr@137',password))
    text_email = binascii.b2a_base64(encrypt('pde%attr@137',email))
    user = Person(first_name=text_name, last_name=text_surname,email=text_email, id=userID,password=text_password,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user', 'first_name': username, 'last_name':surname}
    #print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    found = False
    for i in user:
        print "________________________________________"
        print i.email
        text = binascii.a2b_base64(i.email)
        email = decrypt('pde%attr@137',text)
        if email == userEmail:
            userE = Person.objects.get(id=i.id)
            found = True
        
            
    if found == False:
        return ""
    
    print "but i got here"
    password = decrypt('pde%attr@137',binascii.a2b_base64(userE.password))
    if password == userPassword:
        request.session['user']={'identity':userE.id,'userRole':userE.userRole, 'first_name':userE.first_name, 'last_name':userE.last_name}
        if userE.userRole == 'user':
            data = {
                'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
                'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
                'userID':userE.id,
                'email':decrypt('pde%attr@137',binascii.a2b_base64(userE.email)),
                'userRole':userE.userRole
            }
        elif userE.userRole == 'LEA' or userE.userRole == 'DFI' or userE.userRole == 'SA' :
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
                'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
                'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
                'userID':userE.id,
                'email':decrypt('pde%attr@137',binascii.a2b_base64(userE.email)),
                'userRole':userE.userRole,
                'images':images,
                'audio':audio,
                'video':video,
                'date':str(datetime.date.today())
            }
        else:
            case = personCaseAttribute.objects.filter(person=userE)
            cases = []
            
            for value in case:
                temp = []
                temp.append(value.case.id)
                temp.append(value.case.caseNumber)
                temp.append(value.case.caseName)
                cases.append(temp)

            pde = pdeAttribute.objects.filter(caseAttribute=case[0].case)
            images = []
            audio = []
            video = []
            for val in pde:
                if val.photo:
                    name = val.photo.name
                    sts = name.split('/')
                    images.append({'title': val.title, 'data': sts[1],'id':val.id})
                elif val.audio:
                    name = val.audio.name
                    sts = name.split('/')
                    audio.append({'title': val.title, 'data': sts[1],'id':val.id})
                elif val.video:
                    name = val.video.name
                    sts = name.split('/')
                    video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
            data = {
                'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
                'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
                'userID':userE.id,
                'userRole':userE.userRole,
                'images':images,
                'audio':audio,
                'video':video,
                'case':cases,
                'caseName': case[0].case.caseName,
                'caseNumber': case[0].case.caseNumber,
                'date':str(datetime.date.today())
            }
            
        return data
    else:
        return ""


def UploadAudio(Title,Description,Location,Date,request):
    file = request.FILES['audioFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    print hashed.digest()
    text = binascii.b2a_base64(encrypt('pde%attr@137',hashed.hexdigest()))
    print text
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=text,Person=user,audio=file)
    upload.save()
    audit = AuditLogPDE(person_id=user,action="Added",pde_title=Title,pde_date=datetime.datetime.now(),pde_location=Location,date=datetime.datetime.now())
    audit.save()
    data = {
            'name':decrypt('pde%attr@137',binascii.a2b_base64(user.first_name)),
            'surname':decrypt('pde%attr@137',binascii.a2b_base64(user.last_name)),
            'userID':user.id,
            'email':decrypt('pde%attr@137',binascii.a2b_base64(user.email))
        }
    return data

def UploadVideo(Title,Description,Location,Date,request):
    file = request.FILES['videoFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha1()
    hashed.update(file.read())
    text = binascii.b2a_base64(encrypt('pde%attr@137',hashed.hexdigest()))
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=text,Person=user,video=file)
    upload.save()
    audit = AuditLogPDE(person_id=user,action="Added",pde_title=Title,pde_date=datetime.datetime.now(),pde_location=Location,date=datetime.datetime.now())
    audit.save()
    data = {
            'name':decrypt('pde%attr@137',binascii.a2b_base64(user.first_name)),
            'surname':decrypt('pde%attr@137',binascii.a2b_base64(user.last_name)),
            'userID':user.id,
            'email':decrypt('pde%attr@137',binascii.a2b_base64(user.email))
        }
    return data

def uploadImage(request, title_, description_, location_, date_, userID_):
    image = request.FILES['imageFileUpload']
    
    per = Person.objects.get(id = userID_)
    hashed = hashlib.sha1()
    hashed.update(image.read())
    text = binascii.b2a_base64(encrypt('pde%attr@137',hashed.hexdigest()))
    #plaintext = decrypt('pde%attr@137',text)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print text
    print "++++++++++++++++++++++++++++++++++++++++++++"
    pde = pdeAttribute(title=title_, description=description_, location=location_, date=datetime.datetime.now(),digitalData=text, Person=per, photo=image)
    pde.save()
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print pde.digitalData
    print "++++++++++++++++++++++++++++++++++++++++++++"
    audit = AuditLogPDE(person_id=per,action="Added",pde_title=title_,pde_date=datetime.datetime.now(),pde_location=location_,date=datetime.datetime.now())
    audit.save()
    if per is not None:
        data = {
            'name':decrypt('pde%attr@137',binascii.a2b_base64(per.first_name)),
            'surname':decrypt('pde%attr@137',binascii.a2b_base64(per.last_name)),
            'userID':per.id,
            'email':decrypt('pde%attr@137',binascii.a2b_base64(per.email))
        }
        return data
    else:
        return ""
    
def viewProfile(userID):
    data = []
    
    per = Person.objects.get(id = userID) 
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
            

    data.append(decrypt('pde%attr@137',binascii.a2b_base64(per.first_name)))
    data.append(decrypt('pde%attr@137',binascii.a2b_base64(per.last_name)))
    data.append(per.id)
    data.append(decrypt('pde%attr@137',binascii.a2b_base64(per.email)))
    data.append(photoUploads)
    data.append(videoUploads)
    data.append(audioUploads)
    
    return data

def viewImage(request,image):
    pde = pdeAttribute.objects.get(id=image)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print pde.digitalData
    print "++++++++++++++++++++++++++++++++++++++++++++"
    plaintext = decrypt('pde%attr@137',text)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++"
    hashed = hashlib.sha1()
    hashed.update(pde.photo.read())
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    print "++++++++++++++++++++++++++++++++++++++++++++"
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
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
            'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
            'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':case,
            'imageName':sts[1],
            'arrayCases':list
        }
    
        return data
    else:
        return ""
    

def leaHomePage(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
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
                'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
                'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
                'images':images,
                'audio':audio,
                'video':video,
                'date':str(datetime.date.today())
        }
    return data

def jdyHomePage(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
    case = personCaseAttribute.objects.filter(person=userE)
    cases = []
    for value in case:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)
    print "hahahahahahahahahahahahahah"
    print case
    pde = pdeAttribute.objects.filter(caseAttribute=case[0].case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo:
            name = val.photo.name
            sts = name.split('/')
            images.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.audio:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.video:
            name = val.video.name
            sts = name.split('/')
            video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
    data = {
        'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
        'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': case[0].case.caseName,
        'caseNumber': case[0].case.caseNumber,
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
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print pde.digitalData
    print "++++++++++++++++++++++++++++++++++++++++++++"
    plaintext = decrypt('pde%attr@137',text)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++"
    hashed = hashlib.sha1()
    hashed.update(pde.video.read())
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    print "++++++++++++++++++++++++++++++++++++++++++++"
    if plaintext == hashed:
        userE = Person.objects.get(id=request.session['user']['identity'])
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
            'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
            'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':case,
            'videoName':sts[1],
            'arrayCases':list
        }
    
        return data
    else:
        return ""

def viewAudio(request,audio):
    pde = pdeAttribute.objects.get(id=audio)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print pde.digitalData
    print "++++++++++++++++++++++++++++++++++++++++++++"
    plaintext = decrypt('pde%attr@137',text)
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++"
    hashed = hashlib.sha1()
    hashed.update(pde.audio.read())
    print "++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    print "++++++++++++++++++++++++++++++++++++++++++++"
    
    if plaintext == hashed:
        userE = Person.objects.get(id=request.session['user']['identity'])
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
            'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
            'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
            'title':pde.title,
            'description':pde.description,
            'location':pde.location,
            'date':str(pde.date),
            'caseNumber':case,
            'audioName':sts[1],
            'arrayCases':list
        }
    
        return data
    else:
        return ""

def addCase(case_name, case_number, request):
    user = Person.objects.get(id=request.session['user']['identity'])
    case = caseAttribute(caseName=case_name,caseNumber=case_number,person=user)
    case.save()
    person = personCaseAttribute(person=user,case=case)
    person.save()
    audit = AuditLogCase(person_id=user,action="Added",old_value="None",new_value=case_name,date=datetime.datetime.now())
    audit.save()
    return True

def deletePDE(pde_id,request):
    user = Person.objects.get(id=request.session['user']['identity'])
    pde = pdeAttribute.objects.get(id=pde_id)
    audit = AuditLogPDE(person_id=user,action="Deleted",pde_title=pde.title,pde_date=pde.date,pde_location=pde.location, date=datetime.datetime.now())
    audit.save()
    pde.delete()
    
    return True;

def RegisterAuthorizedUser(request, name, surname, idNo, role, Password, mail):
    text_name = binascii.b2a_base64(encrypt('pde%attr@137',name))
    text_surname = binascii.b2a_base64(encrypt('pde%attr@137',surname))
    text_password = binascii.b2a_base64(encrypt('pde%attr@137',Password))
    text_email = binascii.b2a_base64(encrypt('pde%attr@137',mail))
    user = Person(first_name=text_name, last_name=text_surname, id=idNo, email=text_email,password=text_password, userRole= role)
    user.save()
    return True
    
def viewPdeViaCase(request,ID):
    userE = Person.objects.get(id=request.session['user']['identity'])
    case = personCaseAttribute.objects.filter(person=userE)
    cases = []
    
    for value in case:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)
    print "hahahahahahahahahahahahahah"
    case = caseAttribute.objects.get(id=ID)
    pde = pdeAttribute.objects.filter(caseAttribute=case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo:
            name = val.photo.name
            sts = name.split('/')
            images.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.audio:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.video:
            name = val.video.name
            sts = name.split('/')
            video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
    data = {
        'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
        'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': case.caseName,
        'caseNumber': case.caseNumber,
        'date':str(datetime.date.today())
        }
    return data

def viewByCase(request):
    userE = Person.objects.get(id=request.session['user']['identity'])
    case = personCaseAttribute.objects.filter(person=userE)
    cases = []
            
    for value in case:
        temp = []
        temp.append(value.case.id)
        temp.append(value.case.caseNumber)
        temp.append(value.case.caseName)
        cases.append(temp)

    pde = pdeAttribute.objects.filter(caseAttribute=case[0].case)
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo:
            name = val.photo.name
            sts = name.split('/')
            images.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.audio:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'title': val.title, 'data': sts[1],'id':val.id})
        elif val.video:
            name = val.video.name
            sts = name.split('/')
            video.append({'title': val.title, 'data': sts[1],'id':val.id})
            
    data = {
        'name':decrypt('pde%attr@137',binascii.a2b_base64(userE.first_name)),
        'surname':decrypt('pde%attr@137',binascii.a2b_base64(userE.last_name)),
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': case[0].case.caseName,
        'caseNumber': case[0].case.caseNumber,
        'date':str(datetime.date.today())
    }
            
    return data

    
