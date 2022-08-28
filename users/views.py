from django.http import HttpResponse
from django.template import loader

def dashboard(request):
    template = loader.get_template('dashboard.html')

    context = {}
    return HttpResponse(template.render(context, request))