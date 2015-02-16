from django.shortcuts import render, render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response("web_interface/index.html",
                              locals(),
                              context_instance = RequestContext(request))

