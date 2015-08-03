from .models import *
import datetime
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from simplecrypt import encrypt, decrypt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import hashlib
import binascii

key = hashlib.sha256('0123456789abcdef').digest()
encrytion = AES.new(key)

def pad(s):
    return s+((16-len(s)% 16)*'{')

def encrypt(plain):
    result =encrytion.encrypt(pad(plain))
    return binascii.b2a_base64(result)

def decrypt(cipher):
    ciphertext = binascii.a2b_base64(cipher)
    dec = encrytion.decrypt(ciphertext).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-l]

def encrypt(plain):
    return encrytion.encrypt(pad(plain))

def registerNewUser(userID,username,surname,email,password,request):
    text_name = binascii.b2a_base64(encrypt(username))
    text_surname = binascii.b2a_base64(encrypt(surname))
    text_password = binascii.b2a_base64(encrypt(password))
    text_email = binascii.b2a_base64(encrypt(email))
    user = Person(first_name=text_name, last_name=text_surname,email=text_email, id=userID,password=text_password,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user', 'first_name': username, 'last_name':surname}
    #print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    found = False
    email = ""
    for i in user:
        print "________________________________________"
        print i.email
        text = binascii.a2b_base64(i.email)
        email = decrypt(text)
        if email == userEmail:
            userE = Person.objects.get(id=i.id)
            found = True
        
            
    if found == False:
        return ""
    
    print "but i got here"
    password = decrypt(binascii.a2b_base64(userE.password))
    name=decrypt(binascii.a2b_base64(userE.first_name))
    surname=decrypt(binascii.a2b_base64(userE.last_name))
    if password == userPassword:
        request.session['user']={'identity':userE.id,'userRole':userE.userRole,'first_name':name,'last_name':surname}
        if userE.userRole == 'user':
            data = {
                'name':name,
                'surname':surname,
                'userID':userE.id,
                'email':email,
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
    text = binascii.b2a_base64(encrypt(hashed.hexdigest()))
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=text,Person=user,audio=file)
    upload.save()
    audit = AuditLogPDE(person_id=user,action="Added",pde_title=Title,pde_date=datetime.datetime.now(),pde_location=Location,date=datetime.datetime.now())
    audit.save()
    return True

def UploadAudioLEA(Case,Description,request):
    file = request.FILES['audioFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    print " when uploaded"
    print hashed.hexdigest()
    enc_data = binascii.b2a_base64(encrypt(hashed.hexdigest()))
   
    cases = case.objects.get(id=Case)
    upload = leaDigitalEvidence(description=Description,date=datetime.datetime.now(),digitalData=enc_data,Person=user,case=cases,audio=file)
    upload.save()
    audit = AuditLogDigitalEvidence(case=cases,person_id=user,action="Added",pde_date=datetime.datetime.now(),date=datetime.datetime.now(),pde_description=Description)
    audit.save()
    
    cases = getUserCases(request)
        
    data = {
            'case':cases
        }
    return data

def UploadVideo(Title,Description,Location,Date,request):
    file = request.FILES['videoFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    text = binascii.b2a_base64(encrypt(hashed.hexdigest()))
    upload = pdeAttribute(title=Title,description=Description,location=Location,date=datetime.datetime.now(),digitalData=text,Person=user,video=file)
    upload.save()
    audit = AuditLogPDE(person_id=user,action="Added",pde_title=Title,pde_date=datetime.datetime.now(),pde_location=Location,date=datetime.datetime.now())
    audit.save()
    return True

def UploadVideoLEA(Case,Description,request):
    file = request.FILES['videoFileUpload']
    user = Person.objects.get(id=request.session['user']['identity'])
    
    #public_key = key.publickey()
    #hash = SHA256.new(file.read()).digest()
    #enc_data = public_key.encrypt(hash,32)
    
    hashed = hashlib.sha256()
    hashed.update(file.read())
    enc_data = encrypt(hashed.hexdigest())
    cases = case.objects.get(id=Case)
    upload = leaDigitalEvidence(case=cases,description=Description,date=datetime.datetime.now(),digitalData=binascii.b2a_base64(enc_data),Person=user,video=file)
    upload.save()
    audit = AuditLogDigitalEvidence(case=cases,person_id=user,action="Added",pde_date=datetime.datetime.now(),date=datetime.datetime.now(),pde_description=Description)
    audit.save()
    
    cases= getUserCases(request)
    data = {
            'userID':user.id,
            'case': cases
        }
    return data

def uploadImage(request, title_, description_, location_, date_, userID_):
    image = request.FILES['imageFileUpload']
    
    per = Person.objects.get(id = userID_)
    hashed = hashlib.sha256()
    hashed.update(image.read())
    text = binascii.b2a_base64(encrypt(hashed.hexdigest()))
    pde = pdeAttribute(title=title_, description=description_, location=location_, date=datetime.datetime.now(),digitalData=text, Person=per, photo=image)
    pde.save()
    audit = AuditLogPDE(person_id=per,action="Added",pde_title=title_,pde_date=datetime.datetime.now(),pde_location=location_,date=datetime.datetime.now())
    audit.save()
    return True
    
def uploadImageLEA(request, case_, description_):
    image = request.FILES['imageFileUpload']
    per = Person.objects.get(id=request.session['user']['identity'])
    hashed = hashlib.sha256()
    hashed.update(image.read())
    enc_data = binascii.b2a_base64(encrypt(hashed.hexdigest()))
    cases = case.objects.get(id=case_)

    pde = leaDigitalEvidence(case=cases, description=description_,date=datetime.datetime.now(),digitalData=enc_data, Person=per, photo=image)
    pde.save()
    audit = AuditLogDigitalEvidence(person_id=per,action="Added",pde_date=datetime.datetime.now(),date=datetime.datetime.now(),pde_description=description_,case=cases)
    audit.save()
    cases= getUserCases(request)
   
    data = {
            'userID':per.id,
            'case':cases
        }
    return data

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
            

    data.append(decrypt(binascii.a2b_base64(per.first_name)))
    data.append(decrypt(binascii.a2b_base64(per.last_name)))
    data.append(per.id)
    data.append(decrypt(binascii.a2b_base64(per.email)))
    data.append(photoUploads)
    data.append(videoUploads)
    data.append(audioUploads)
    
    return data

def viewImage(request,image):
    pde = pdeAttribute.objects.get(id=image)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.photo.read())
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
    return True;

def viewVideo(request,video):
    pde = pdeAttribute.objects.get(id=video)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.video.read())
    if plaintext == hashed.hexdigest():
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
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.audio.read())
    
    if plaintext == hashed.hexdigest():
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
    
    return True

def RegisterAuthorizedUser(request, name, surname, idNo, role, Password, mail):
    text_name = binascii.b2a_base64(encrypt(name))
    text_surname = binascii.b2a_base64(encrypt(surname))
    text_password = binascii.b2a_base64(encrypt(Password))
    text_email = binascii.b2a_base64(encrypt(mail))
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
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': case[0].case.caseName,
        'caseNumber': case[0].case.caseNumber,
        'date':str(datetime.date.today())
    }
            
    return data

def getUserCases(request):
    per = Person.objects.get(id=request.session['user']['identity'])
    Pcase = personCase.objects.filter(person=per)
    
    cases = []
    for x in Pcase:
        data = []
        data.append(x.case.id)
        data.append(x.case.caseName)
        data.append(x.case.caseNumber)
        cases.append(data)
    
    return cases
        
def Documentation(request):
    per = Person.objects.get(id=request.session['user']['identity'])
    cases = getUserCases(request)
    
    case1 = cases[0]
    caseObj = case.objects.get(id=case1[0])
    pde = leaDigitalEvidence.objects.filter(case=caseObj)
    
    images = []
    audio = []
    video = []
    for val in pde:
        if val.photo:
            name = val.photo.name
            sts = name.split('/')
            images.append({'data': sts[1],'id':val.id})
        elif val.audio:
            name = val.audio.name
            sts = name.split('/')
            audio.append({'data': sts[1],'id':val.id})
        elif val.video:
            name = val.video.name
            sts = name.split('/')
            video.append({'data': sts[1],'id':val.id})
            
    data = {
        'images':images,
        'audio':audio,
        'video':video,
        'case':cases,
        'caseName': caseObj.caseName,
        'caseNumber': caseObj.caseNumber,
        'date':str(datetime.date.today())
    }
    return data

def viewImageLEA(request,image):
    pde = leaDigitalEvidence.objects.get(id=image)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.photo.read())
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    if plaintext == hashed.hexdigest():
        print "AM IN HERE, BUT I DNT KNOW HOW"
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.photo.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'case-description':pde.case.description,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'incident': str(pde.case.date),
            'caseName': caseN, 
            'caseNumber':cases,
            'imageName':sts[1],
            'arrayCases':list
        }
    
        return data
    else:
        return ""
    
def viewAudioLEA(request,audio):
    pde = leaDigitalEvidence.objects.get(id=audio)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.audio.read())
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    if plaintext == hashed.hexdigest():
        print "AM IN HERE, BUT I DNT KNOW HOW"
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.audio.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'case-description':pde.case.description,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'incident': str(pde.case.date),
            'caseName': caseN, 
            'caseNumber':cases,
            'audioName':sts[1],
            'arrayCases':list
        }
    
        return data
    else:
        return ""

def viewVideoLEA(request,video):
    pde = leaDigitalEvidence.objects.get(id=video)
    encypted = pde.digitalData
    text = binascii.a2b_base64(encypted)
    plaintext = decrypt(text)
    hashed = hashlib.sha256()
    hashed.update(pde.video.read())
    print plaintext
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print hashed.hexdigest()
    if plaintext == hashed.hexdigest():
        userE = Person.objects.get(id=request.session['user']['identity'])
        cases = None
        caseN = None
        if pde.case:
            cases = pde.case.caseNumber
            caseN = pde.case.caseName
    
        Iname = pde.video.name
        sts = Iname.split('/')
    
        caseObj = case.objects.all()
        list = []
        for i in caseObj:
            list1 = []
            list1.append(i.caseNumber)
            list1.append(i.id)
            list.append(list1)
    
        data = {
            'title':pde.case.title,
            'case-description':pde.case.description,
            'description': pde.description,
            'location':pde.case.location,
            'date':str(pde.date),
            'incident': str(pde.case.date),
            'caseName': caseN, 
            'caseNumber':cases,
            'videoName':sts[1],
            'arrayCases':list
        }
    
        return data
    else:
        return ""
    
def assignCaseLEA(pdeID,caseID):
    pde = leaDigitalEvidence.objects.get(id=pdeID)
    cases = case.objects.get(id=caseID)
    
    pde.case = cases
    pde.save()
    return True;

def deletePDE_LEA(pde_id,request):
    user = Person.objects.get(id=request.session['user']['identity'])
    pde = leaDigitalEvidence.objects.get(id=pde_id)
    audit = AuditLogDigitalEvidence(person_id=user,action="Deleted",pde_date=pde.date, pde_description= pde.description, date=datetime.datetime.now())
    audit.save()
    pde.delete()
    
    return True

def Search(request,case_id):
    cases = case.objects.get(id=case_id)
    pde = pdeAttribute.objects.fitler(date=cases.date,location=cases.location)
    
    final = []
    
    for i in pde:
        temp = []
        temp.aapend(pde.id)
        temp.append(pde.title)
        if pde.photo:
            name = value.photo.name
            sts = name.split('/')
            temp.append(sts[1])
        elif pde.audio:
            name = value.audio.name
            sts = name.split('/')
            temp.append(sts[1])
        else:
            name = value.video.name
            sts = name.split('/')
            temp.append(sts[1])
        final.append(temp)
    
    return final
    
    


