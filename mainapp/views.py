from django.http import HttpResponse
from django.template import loader
from .models import *

def index(request):
    template = loader.get_template('index.html')

    articles = Article.objects.all()
    context = {
        'articles': articles,
    }

    if request.user.is_authenticated:
        custom_user = Author.objects.get(user=request.user)
        context['custom_user'] = custom_user
        
    return HttpResponse(template.render(context, request))

def article(request, article_id):
    template = loader.get_template('article.html')
    article = Article.objects.get(id=article_id)

    context = {
        'article': article,
    }
    return HttpResponse(template.render(context, request))

def add_article(request):
    template = loader.get_template('add_article.html')

    if request.method == "POST":
        author = Author.objects.get(user=request.user)
        img = request.POST['image']
        text = request.POST['text']
        new_article = Article(author=author, text=text, image=img)
        new_article.save()

    context = {}
        
    return HttpResponse(template.render(context, request))