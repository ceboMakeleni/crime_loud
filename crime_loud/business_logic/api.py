from .models import *

def registerNewUser(userID,username,surname,email,password,usercell,request):
    user = Person(first_name=username, last_name=surname,email=email, identity=userID,password=password,cell_number=usercell,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user'}
    #print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    for i in user:
        if i.email == userEmail:
            userE = Person.objects.get(email=userEmail)
            
    if userEmail == "":
        return ""
    print "but i got here"
    if userE.password == userPassword:
        request.session['user']={'identity':userE.identity,'userRole':userE.userRole}
        data = {
            'name':userE.first_name,
            'surname':userE.last_name,
            'userID':userE.identity,
            'cellNo':userE.cell_number,
            'email':userE.email
        }
        return data
    else:
        return ""


    
