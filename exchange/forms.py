from django import forms
from . import models

#choices = Category.objects.all().values_list('name', flat=True)
#choice_list = list(choices)

#categories = Category.objects.all()
#choices = [category.name for category in categories]


class CreatePost(forms.ModelForm):
    # Which fields we want to be present, from which model it is inheriting
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'slug', 'thumb']

        # widgets = {
        #    'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
        #}
        # Add tags functionality
