import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from web_services import views
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render_to_response("web_interface/index.html",
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
        
        if res[0]['type'] == 1:
            return render_to_response("web_interface/x.htm")
        
        else:
            return render_to_response("web_interface/y.htm")
    
