import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt

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
    
    if request.method == "POST":
        data = {
                'userID' : userID,
                'userName': userName,
                'userSurname': userSurname,
                'userEmail': userEmail,
                'userPassword': userPassword
            }
        
        results = views.registerNewUser(request, json.dumps(data))
        res = json.loads (results.content)
        
        name = res['name']
        
        
        if res['type'] == 1:
            return render_to_response("web_interface/landing.html", { 'name':name})
        
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
            return render_to_response("web_interface/landing.html")
        else:
            return render_to_response("web_interface/login.html")
        
    else:
        print "Web_interface views: login --- GET method instead of POST used"
        return Http404()