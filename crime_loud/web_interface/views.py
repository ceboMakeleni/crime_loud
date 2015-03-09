import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt
from crime_loud.settings import MEDIA_ROOT

def home(request):
    return render_to_response("web_interface/login.html",
                              locals(),
                              context_instance = RequestContext(request))

@csrf_exempt
def registerNewUser(request):
    userID = request.POST['registerID']
    userName = request.POST['registerName']
    userSurname = request.POST['registerSurname']
    userEmail = request.POST['registerEmail']
    userPassword = request.POST['registerPassword']
    userCell = request.POST['registerCell']
    
    if request.method == "POST":
        data = {
                'userID' : userID,
                'userName': userName,
                'userSurname': userSurname,
                'userEmail': userEmail,
                'userPassword': userPassword,
                'userCell':userCell
            }
        
        results = views.registerNewUser(request, json.dumps(data))
        res = json.loads (results.content)
        
        name = res['name']
        
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html", { 'name':name,
                                                                     'surname':res['userSurname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['userEmail'],
                                                                     'cellNo':res['userCell']})
        
        else:
            return render_to_response("web_interface/login.html", { 'name':name})
    else:
        print "Web_interface views: registerNewUser --- GET method instead of POST used"
        return Http404()
    
@csrf_exempt
def login(request):
    userEmail =request.POST['loginEmail']
    userPassword = request.POST['loginPassword']
    
    if request.method == 'POST':
        data = {
            'userEmail':userEmail,
            'userPassword':userPassword
        }
        
        results = views.login(request, json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            if res['userRole'] == 'user':
                return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'userID':res['userID'],
                                                                         'userEmail':res['email'],
                                                                         'cellNo':res['cellNo']})
            elif res['userRole'] == 'LEA' or res['userRole'] == 'DFI' :
                return render_to_response("web_interface/law_enforcement.html",{ 'name':res['name'],
                                                                         'surname':res['surname'],
                                                                         'userID':res['userID'],
                                                                         'userEmail':res['email'],
                                                                         'cellNo':res['cellNo'],'images':res['images'],
                                                                         'audio':res['audio'],'video':res['video'], 'date':res['date']})
            elif res['userRole'] == 'JDY':
                pass
            elif res['userRole'] == 'SA':
                pass
        else:
            return render_to_response("web_interface/login.html")
        
    else:
        print "Web_interface views: login --- GET method instead of POST used"
        return Http404()
    
@csrf_exempt
def imageUpload(request):
    title = request.POST['imageTitle']
    description = request.POST['imageDescription']
    location = request.POST['imageLocation']
    date = request.POST['imageDate']
    
    userID = request.session['user']['identity']
   
    data = {
        'title':title,
        'description': description,
        'location':location,
        'date':date,
        'userID':userID,
    }

    results = views.imageUpload(request, json.dumps(data))
    res = json.loads(results.content)
    
    return render_to_response("web_interface/landing.html",{'type':res['type'], 'name':res['name'],
                                                            'surname':res['surname'], 'cell':res['cell'],
                                                            'userID':res['userID'], 'email':res['email']})

def viewProfile(request):
    userID = request.session['user']['identity']
    
    data = {
        'userID':userID
    }
    results = views.viewProfile(request, json.dumps(data))
    res = json.loads(results.content)
    
    
    return render_to_response("web_interface/profile.html",{'type':res['type'], 'name':res['name'],
                                                            'surname':res['surname'], 'cell':res['cell'],
                                                            'userID':res['userID'], 'email':res['email'],
                                                            'photoUploads':res['photoUploads'], 'videoUploads':res['videoUploads'],
                                                            'audioUploads':res['audioUploads']})
    
def backHome(request):
    userRole = request.session['user']['userRole']
    name = request.session['user']['first_name']
    surname = request.session['user']['last_name']
    if userRole == 'user':
        return render_to_response("web_interface/landing.html",{'name':name, 'surname':surname} )
    elif userRole == 'LEA' or userRole == 'DFI':
        return render_to_response("web_interface/law_enforcement.html",{'name':name, 'surname':surname} )
    elif userRole == 'JDY':
        pass
    elif userRole == 'SA':
        pass

@csrf_exempt
def UploadAudio(request):
    if request.method == 'POST':
        title = request.POST['audioTitle']
        description = request.POST['audioDescription']
        location = request.POST['audioLocation']
        date = request.POST['audioDate']
        filename = request.FILES['audioFileUpload']
        
        data = {
            'title':title,
            'description':description,
            'location':location,
            'date':date,
        }
        
        results = views.UploadAudio(request,json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['email'],
                                                                     'cellNo':res['cellNo']})
        else:
            return render_to_response("web_interface/landing.html", { 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['email'],
                                                                     'cellNo':res['cellNo']})

@csrf_exempt
def UploadVideo(request):
    if request.method == 'POST':
        title = request.POST['videoTitle']
        description = request.POST['videoDescription']
        location = request.POST['videoLocation']
        date = request.POST['videoDate']
        filename = request.FILES['videoFileUpload']
        
        data = {
            'title':title,
            'description':description,
            'location':location,
            'date':date,
        }
        
        results = views.UploadVideo(request,json.dumps(data))
        res = json.loads(results.content)
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['email'],
                                                                     'cellNo':res['cellNo']})
        else:
            return render_to_response("web_interface/landing.html", { 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['email'],
                                                                     'cellNo':res['cellNo']})
def logout(request):
    request.session.delete()      
    return render_to_response("web_interface/login.html")

def takePhoto(request):  
    return render_to_response("web_interface/takePhoto.html")

