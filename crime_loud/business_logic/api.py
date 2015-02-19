from .models import *

def registerNewUser(userID,username,surname,email,password,request):
    user = Person(first_name=username, last_name=surname,email=email, identity=userID,password=password,userRole='user')
    user.save()
    
    request.session['user']={'identity':userID,'userRole':'user'}
    print request.session['user']
    return True

def login(userEmail, userPassword,request):
    user = Person.objects.all()
    userE = ""
    for i in user:
        if i.email == userEmail:
            userE = Person.objects.get(email=userEmail)
            
    if userEmail == "":
        return False
    print "but i got here"
    if userE.password == userPassword:
        request.session['user']={'identity':userE.identity,'userRole':userE.userRole}
        return True
    else:
        return False

def profile():
    pass
    
