from django.shortcuts import redirect, render
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView


def like(request, pk):
    print('this is post id' + request.POST.get('post_id'))
    post = get_object_or_404(Article, id=request.POST.get('post_id'))
     # id is getting the post_id assigned in the article_detail html form, retrieving it, and looking in the Article table
    post.likes.add(request.user) # Save the user's like in the database
     # return redirect('articles:detail')
    return HttpResponseRedirect(reverse('articles:detail', args=[str(pk)]))


def index(response):
    return render(response, "exchange/index.html", {})


def home(response):
    return render(response, "exchange/home.html", {})


def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, "exchange/travelPage.html", {'articles': articles})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'exchange/article_detail.html'

'''
def article_details(request, slug):  # Save the slug of what page the use wants to go to
    # return HttpResponse(slug)
    print(slug)
    article = Article.objects.get(slug=slug)
    # article = get_object_or_404(Article, slug=slug)
    return render(request, "exchange/article_detail.html", {'article': article})
'''

@login_required(login_url="/accounts/signin/")
# View function to handle creation of new articles
def article_create(request):
    # If the request method is POST, process the form submission
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = forms.CreatePost(request.POST, request.FILES)
        # If the form is valid, save the article to the database
        if form.is_valid():
            # save article to database
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:travelPage')
    else:
        form = forms.CreatePost()
    return render(request, 'exchange/article_create.html', {'form': form})


