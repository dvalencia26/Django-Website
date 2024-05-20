from django import forms
from . import models
from .models import Thread
#categories = Category.objects.all()
#choices = [category.name for category in categories]


class CreatePost(forms.ModelForm):
    # Which fields we want to be present, from which model it is inheriting
    class Meta:
        model = models.Article
        fields = ['title', 'country', 'tags', 'body', 'thumb']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Add comment ...'})
        }
        labels = {
            'body': ''
        }


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'subcategory', 'body']
