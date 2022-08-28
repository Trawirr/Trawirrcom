from django.http import HttpResponse
from django.template import loader
from .models import *

def index(request):
    template = loader.get_template('index.html')

    context = {}

    if request.user.is_authenticated:
        custom_user = Author.objects.get(user=request.user)
        context['custom_user'] = custom_user
        
    return HttpResponse(template.render(context, request))

def article(request, article_id):
    pass

def add_article(request):
    pass