import json
import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.context_processors import csrf
from business_logic import api

def registerNewUser(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    userID = json_data['userID']
    userName = json_data['userName']
    userSurname = json_data['userSurname']
    userEmail = json_data['userEmail']
    userPassword = json_data['userPassword']
    
    result = api.registerNewUser(userID, userName, userSurname, userEmail, userPassword,request)
    result = True
    
    if result == True:
        data = {
            'type':1,
            'name': userName
        }
    
    else:
        data = {
            'type':-1,
            'name':userName
        }
    
    return HttpResponse(json.dumps(data))

def login(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    userEmail = json_data['userEmail']
    userPassword = json_data['userPassword']
    
    result = api.login(userEmail, userPassword,request)
    
    if result == True:
        data = {
            'type':1
        }
        
    else:
        data = {
            'type': -1
        }
        
    return HttpResponse(json.dumps(data))

    
    
   

