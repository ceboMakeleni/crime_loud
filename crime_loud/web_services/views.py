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
    userCell = json_data['userCell']
    
    result = api.registerNewUser(userID, userName, userSurname, userEmail, userPassword,userCell,request)
    result = True
    
    if result == True:
        data = {
            'type':1,
            'name': userName,
            'userID':userID,
            'userSurname':userSurname,
            'userEmail':userEmail,
            'userCell':userCell
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
    
    if result != "":
        if request.session['user']['userRole'] == 'user':
            data = {
                'type':1,
                'name':result['name'],
                'surname':result['surname'],
                'userID':result['userID'],
                'cellNo':result['cellNo'],
                'email':result['email'],
                'userRole':result['userRole']
            }
        else:
            data = {
                'type':1,
                'name':result['name'],
                'surname':result['surname'],
                'userID':result['userID'],
                'cellNo':result['cellNo'],
                'email':result['email'],
                'userRole':result['userRole'],
                'images':result['images'],
                'audio': result['audio'],
                'video': result['video'],
                'date': result['date']
            }
        
    else:
        data = {
            'type': -1
        }
        
    return HttpResponse(json.dumps(data))


def imageUpload(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    title = json_data['title']
    description = json_data['description']
    location = json_data['location']
    date = json_data['date']
    userID = json_data['userID']
    
    
    result = api.uploadImage(request, title, description, location, date, userID)
    
    if result is not None:
        data = {
            'type':1,
            'name':result['name'],
            'surname':result['surname'],
            'userID':result['userID'],
            'cell':result['cellNo'],
            'email': result['email']
        }
        
    else:
        data = {
            'type':-1,
            'name':result['name'],
            'surname':result['surname'],
            'userID':result['userID'],
            'cell':result['cellNo'],
            'email': result['email']
        }
    
    return HttpResponse(json.dumps(data))

def viewProfile(request, jsonObj):
    json_data = json.loads(jsonObj)
    userID = json_data['userID']
    
    result = api.viewProfile(userID)
    
    if result != []:
        data = {
            'type':1,
            'name':result[0],
            'surname':result[1],
            'userID':result[2],
            'cell':result[3],
            'email':result[4],
            'photoUploads':result[5],
            'videoUploads':result[6],
            'audioUploads':result[7]
        }
    else:
        data = {
            'type':-1, #person could not be located in database
        }
        
    return HttpResponse(json.dumps(data))

    
def UploadVideo(request, jsonObj):
    json_data = json.loads(jsonObj)
    
    title = json_data['title']
    description = json_data['description']
    location = json_data['location']
    date = json_data['date']
    #file = json_data['file']
    
    result = api.UploadVideo(title,description,location,date,request)
    if result != "":
        data = {
            'type':1,
            'name':result['name'],
            'surname':result['surname'],
            'userID':result['userID'],
            'cellNo':result['cellNo'],
            'email':result['email']
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':result['name'],
            'surname':result['surname'],
            'userID':result['userID'],
            'cellNo':result['cellNo'],
            'email':result['email']
        }
        return HttpResponse(json.dumps(data))
    
    
def UploadAudio(request, jsonObj):
    json_data = json.loads(jsonObj)
    title = json_data['title']
    description = json_data['description']
    location = json_data['location']
    date = json_data['date']
    #file = json_data['file']
    result = api.UploadAudio(title,description,location,date,request)
    if result != "":
        data = {
            'type':1,
            'name':result['name'],
            'surname':result['surname'],
            'userID':result['userID'],
            'cellNo':result['cellNo'],
            'email':result['email']
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type':-1,
            'name':result['name'],
            'surname':result['surname'],
            'userID':result['userID'],
            'cellNo':result['cellNo'],
            'email':result['email']
        }
        return HttpResponse(json.dumps(data))
    
   

