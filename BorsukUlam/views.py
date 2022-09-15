from django.http import HttpResponse
from django.template import loader
from .models import *

from .utils.borsukulam import *

def index(request):
    template = loader.get_template('borsukulam.html')

    context = {
    }
    return HttpResponse(template.render(context, request))