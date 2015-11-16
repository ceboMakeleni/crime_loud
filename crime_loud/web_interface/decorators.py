#from django.http import *
#from django.shortcuts import render_to_response
#from django.template import loader, RequestContext
#from django.core.urlresolvers import reverse
#import json
#
#def isLawEnforcementAgent(function):
#    def wrapper(request,*args,**kwargs):
#        userRole = request.session['user']['userRole']
#        if userRole == 'LEA':
#             return function(request,*args,**kwargs)
#        else:
#            del request.session['user']
#            return HttpResponseRedirect(reverse('logout'))
#    return wrapper