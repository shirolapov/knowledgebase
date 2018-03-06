from django.conf.urls import url
from articles.views import (list_of_articles, page_of_articles, new_article,
                           new_article_success, change_article, delete_article)

app_name = 'articles'
urlpatterns = [
    url(r'change/(?P<id>[0-9]+)/', change_article, name='change'),
    url(r'delete/(?P<id>[0-9]+)/', delete_article, name='delete'),
    url(r'new/success/$', new_article_success, name = 'new_article_success'),
    url(r'new/$', new_article, name = 'new'),
    url(r'(?P<id>[0-9]+)/', page_of_articles, name='page'),
    url(r'$', list_of_articles, name='list'),
]
