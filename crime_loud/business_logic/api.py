from .models import *

def registerNewUser(userID,username,surname,email,password):
    user = Person(first_name=username, last_name=surname,email=email, identity=userID,password=password,userRole='user')
    user.save();
    return True;

def login(userEmail, userPassword):
    user = Person.objects.all()
    userE = ""
    for i in user:
        if i.email == userEmail:
            userE = Person.objects.get(email=userEmail)
            
    if userEmail == "":
        return False
    print "but i got here"
    if userE.password == userPassword:
        return True;
    else:
        return False;
    