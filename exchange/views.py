from django.shortcuts import redirect, render
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms


def index(response):
    return render(response, "exchange/index.html", {})


def home(response):
    return render(response, "exchange/home.html", {})


def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request,"exchange/travelPage.html", {'articles': articles})


def article_details(request, slug): # Save the slug of what page the use wants to go to
    # return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    return render(request, "exchange/article_detail.html", {'article':article})


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


