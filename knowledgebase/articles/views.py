import json
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from articles.models import Article
from articles.forms import ArticleForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def list_of_articles(request):
    is_login = False
    user = None

    if request.user.is_authenticated():
        articles = Article.objects.all().order_by("-datetime_created")
        is_login = True
        user = request.user
    else:
        articles = Article.objects.filter(
            internal=False
        ).order_by("-datetime_created")

    paginator = Paginator(articles, 5)

    page = request.GET.get('page')

    try:
        articles_p = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles_p = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles_p = paginator.page(paginator.num_pages)

    context = {
        "header": {
            "title": "Лента статей"
        },
        "articles": articles_p,
        "is_login": is_login,
        "user": user
    }
    template = loader.get_template('articles/allarticles.html')
    return HttpResponse(template.render(context, request))


def page_of_articles(request, id):
    is_login = False
    user = None
    views_author = False

    article = get_object_or_404(Article, id = id)
    if article.internal:
        if not request.user.is_authenticated():
            return HttpResponseForbidden("Доступ запрещён")
        else:
            title = u"Статья {title}".format(title=article.title)
            is_login = True
            user = request.user
            views_author = article.author == user

    context = {
        "header": {
            "title": title
        },
        "article": article,
        "views_author": views_author,
        "is_login": is_login,
        "user": user
    }
    template = loader.get_template('articles/article.html')
    return HttpResponse(template.render(context, request))


@login_required
def new_article(request):
    is_login = True
    user = request.user

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
        "header": {
            "title": "Создать новую статью"
        },
        "form": form,
        "is_login": is_login,
        "user": user
    }
    template = loader.get_template('articles/newarticle.html')
    return HttpResponse(template.render(context, request))


@login_required
def new_article_success(request):
    new_article_created = False
    is_login = True
    user = request.user

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
            "article": article,
            "is_login": is_login,
            "user": user
        }
        template = loader.get_template('articles/successcreated.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect(reverse('articles:new'))


@login_required
def change_article(request, id):
    changed = False
    is_login = True
    user = request.user

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            id = request.POST["id_article"]
            article = get_object_or_404(Article, id = id)
            article.title = form.cleaned_data["title"]
            article.short_text = form.cleaned_data["short_text"]
            article.text = form.cleaned_data["text"]
            article.internal = form.cleaned_data["internal"]
            article.save()
            changed = True

    if changed:
        article = article
    else:
        article = get_object_or_404(Article, id = id)

    title = u"Изменение статьи {title}".format(title=article.title)
    form = ArticleForm(instance=article)
    context = {
        "header": {
            "title": title,
        },
        "article": article,
        "form": form,
        "changed": changed,
        "is_login": is_login,
        "user": user
    }
    template = loader.get_template('articles/changearticle.html')
    return HttpResponse(template.render(context, request))


@login_required
def delete_article(request, id):
    is_login = True
    user = request.user

    if request.method == 'POST':
        article = get_object_or_404(Article, id = id)
        if user == article.author:
            article.delete()
            context = {
                "header": {
                    "title": "Статья успешно удалена",
                },
                "is_login": is_login,
                "user": user
            }
            template = loader.get_template('articles/successdeleted.html')
            return HttpResponse(template.render(context, request))
