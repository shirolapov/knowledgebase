import json
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from articles.models import Article
from articles.forms import ArticleForm


# Create your views here.
def list_of_articles(request):
    if request.user.is_authenticated():
        articles = Article.objects.all().order_by("-datetime_created")
    else:
        articles = Article.objects.filter(
            internal=False
        ).order_by("-datetime_created")

    context = {
        "articles": articles
    }
    template = loader.get_template('articles/allarticles.html')
    return HttpResponse(template.render(context, request))


def page_of_articles(request, id):
    article = get_object_or_404(Article, id = id)
    if article.internal:
        if not request.user.is_authenticated():
            return HttpResponseForbidden("Доступ запрещён")

    context = {
        "article": article,
        "views_Author": True
    }
    template = loader.get_template('articles/article.html')
    return HttpResponse(template.render(context, request))


@login_required
def new_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article.objects.create(
                author = request.user,
                title = form.cleaned_data['title'],
                short_text = form.cleaned_data['short_text'],
                text = form.cleaned_data['text'],
                internal = form.cleaned_data['internal']
            )
            article.save()
            request.session['new_article'] = json.dumps(True)
            request.session['last_created_article'] = json.dumps(article.id)
            return redirect(reverse('articles:new_article_success'))


    form = ArticleForm()
    context = {
        "form": form
    }
    template = loader.get_template('articles/newarticle.html')
    return HttpResponse(template.render(context, request))


@login_required
def new_article_success(request):
    new_article_created = False
    try:
        new_article_created = json.loads(request.session['new_article'])
        last_created_article_id = json.loads(
            request.session['last_created_article']
        )
    except KeyError:
        pass

    if new_article_created:
        request.session['new_article'] = False
        article = get_object_or_404(Article, id = last_created_article_id)
        context = {
            "article": article
        }
        template = loader.get_template('articles/successcreated.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect(reverse('articles:new'))


@login_required
def change_article(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(instance=article)
    context = {
        "article": article,
        "form": form
    }
    template = loader.get_template('articles/changearticle.html')
    return HttpResponse(template.render(context, request))
