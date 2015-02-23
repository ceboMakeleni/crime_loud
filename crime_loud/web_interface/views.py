import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt
from crime_loud.settings import MEDIA_ROOT
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

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
            return render_to_response("web_interface/landing.html",{ 'name':res['name'],
                                                                     'surname':res['surname'],
                                                                     'userID':res['userID'],
                                                                     'userEmail':res['email'],
                                                                     'cellNo':res['cellNo']})
        else:
            return render_to_response("web_interface/login.html")
        
    else:
        print "Web_interface views: login --- GET method instead of POST used"
        return Http404()

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
            'file': filename.name
        }
        #path = default_storage.save(MEDIA_ROOT, ContentFile(file.read()))
        fd = open(MEDIA_ROOT, 'wb')
        fd.write(filename.content)
        fd.close()
        
        results = views.UploadAudio(request,json.dump(data))
        res = json.loads(results)
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html")
        else:
            return render_to_response("web_interface/landing.html")

        
