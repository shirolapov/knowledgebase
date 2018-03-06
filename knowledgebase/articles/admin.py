from django.contrib import admin
from articles.models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'internal', 'datetime_created', 'author')
    list_filter = ('internal', 'author')
    fields = ('author', 'title', 'short_text', 'text', 'internal',
              'datetime_created', 'datetime_modified')
    readonly_fields = ('datetime_created', 'datetime_modified')


admin.site.register(Article, ArticleAdmin)
