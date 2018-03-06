from django.forms import ModelForm, Textarea, TextInput, BooleanField, CheckboxInput
from articles.models import Article
from redactor.widgets import RedactorEditor


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'short_text', 'text', 'internal']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'short_text': Textarea(attrs={'class': 'form-control'}),
            'text': RedactorEditor(attrs={'class': 'form-control'}),
            'internal': CheckboxInput(attrs={'class': 'form-control'}),
        }
