from django.contrib.auth.models import User
from django.db import models
from redactor.fields import RedactorField

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = u"Автор"
    )
    title = models.CharField(
        max_length = 250,
        verbose_name = u"Заголовок"
    )
    short_text = models.TextField(
        verbose_name=u"Короткий текст",
        blank=True,
        help_text = u"Этот текст будет виден на главной странице"
    )
    text = RedactorField(
        verbose_name = u"Текст",
        help_text = u"Этот текст будет виден толкьо после перхода на страницу статьи"
    )
    internal = models.BooleanField(
        default = True,
        verbose_name = u"Только для сотрудников"
    )
    datetime_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u"Время создания"
    )
    datetime_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=u"Время изменения"
    )

    def __str__(self):
        return self.title

    def get_author(self):
        if self.author.last_name == "" or  self.author.first_name == "":
            return self.author.username
        else:
            return "{firstname} {lastname}".format(
                firstname = self.author.first_name,
                lastname = self.author.last_name
            )

    class Meta:
        verbose_name = u"Статья"
        verbose_name_plural = u"Статьи"
