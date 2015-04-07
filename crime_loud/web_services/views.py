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
    
def viewImage(request,jsonObj):
    json_data = json.loads(jsonObj)
    image_id = json_data['image']
    
    result = api.viewImage(request,image_id)
    if result:
        data={
            'type':1,
            'name':result['name'],
            'surname':result['surname'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'imageName':result['imageName'],
            'cases':result['arrayCases']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(result)
        data = {
            'type':-1,
            'name':res['name'],
            'surname':res['surname'],
            'images':res['images'],
            'audio': res['audio'],
            'video': res['video'],
            'date': res['date']
        }
        return HttpResponse(json.dumps(data))

def assignCase(request,jsonObj):
    json_data = json.loads(jsonObj)
    case = json_data['case']
    pde = json_data['pde']
    
    result = api.assignCase(pde,case)
    
    if result:
        data ={
            'type': 1
        }
    else:
        data = {
            'type':-1
        }
    
    return HttpResponse(json.dumps(data))
    
def leaHomePage(request):
        res = api.leaHomePage(request)
        
        data = {
            'type':1,
            'name':res['name'],
            'surname':res['surname'],
            'images':res['images'],
            'audio': res['audio'],
            'video': res['video'],
            'date': res['date']
        }
        
        return HttpResponse(json.dumps(data))

def viewVideo(request,jsonObj):
    json_data = json.loads(jsonObj)
    video_id = json_data['image']
    
    result = api.viewVideo(request,video_id)
    if result:
        data={
            'type':1,
            'name':result['name'],
            'surname':result['surname'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'videoName':result['videoName'],
            'cases':result['arrayCases']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(result)
        data = {
            'type':-1,
            'name':res['name'],
            'surname':res['surname'],
            'images':res['images'],
            'audio': res['audio'],
            'video': res['video'],
            'date': res['date']
        }
        return HttpResponse(json.dumps(data))
    
def viewAudio(request,jsonObj):
    json_data = json.loads(jsonObj)
    video_id = json_data['audio']
    
    result = api.viewAudio(request,video_id)
    if result:
        data={
            'type':1,
            'name':result['name'],
            'surname':result['surname'],
            'title': result['title'],
            'description':result['description'],
            'location':result['location'],
            'date':result['date'],
            'caseNumber': result['caseNumber'],
            'audioName':result['audioName'],
            'cases':result['arrayCases']
        }
        
        return HttpResponse(json.dumps(data))
    else:
        res = api.leaHomePage(result)
        data = {
            'type':-1,
            'name':res['name'],
            'surname':res['surname'],
            'images':res['images'],
            'audio': res['audio'],
            'video': res['video'],
            'date': res['date']
        }
        return HttpResponse(json.dumps(data))

def addCase(request,jsonObj):
    json_data = json.loads(jsonObj)
    name = json_data['name']
    number = json_data['number']
    
    result = api.addCase(name,number,request)
    if result:
        data = {
            'type': 1,
        }
        return HttpResponse(json.dumps(data))
    else:
        data = {
            'type': -1
        }
        return HttpResponse(json.dumps(data))
    
def deletePDE(request,jsonObj):
    json_data = json.loads(jsonObj)
    pde = json_data['id']
    
    result = api.deletePDE(pde,request)
    if result:
        data = {
            'type':1
        }
        return HttpResponse(json.dumps(data))
    else:
        data ={
            'type':-1
        }
        return HttpResponse(json.dumps(data))

def registerAuthorzedUser(request, jsonObj):
    json_data = json.loads(jsonObj)
    name = json_data['name']
    surname = json_data['surname']
    email = json_data['email']
    cell = json_data['cell']
    idNo = json_data['idNo']
    role = "LEA"
    password = json_data['password']
    
    results = api.RegisterAuthorizedUser(request, name)
    