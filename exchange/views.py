from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib import messages


@login_required(login_url="/accounts/signin/")
def like(request, pk):
    # Handles the like functionality for articles
    post = get_object_or_404(Article, id=request.POST.get('post_id'))
    # id is getting the post_id assigned from the article_detail html form, retrieving it, and looking in the Article table
    post.likes.add(request.user)  # Save the user's like in the database
    return HttpResponseRedirect(reverse('articles:detail', args=[str(pk)]))


def index(response):
    # Displays a list of countries excluding 'default' and their related articles
    country_lists = Country.objects.exclude(name='default').prefetch_related('article_set')
    country_articles = []

    # Loop that helps with the images display in the index(home) page
    for country in country_lists:
        articles = country.article_set.all()[:4]
        country_articles.append((country, articles))

    context = {
        "country_articles": country_articles
    }

    return render(response, "exchange/index.html", context)


#def home(response):
#    return render(response, "exchange/home.html", {})


def article_list(request):
    # Displays a list of all articles ordered by date
    articles = Article.objects.all().order_by('date')
    return render(request, "exchange/travelPage.html", {'articles': articles})

class ArticleDetailView(DetailView):
    # Detail view for a specific article
    model = Article
    template_name = 'exchange/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = self.get_object()
        like_data = get_object_or_404(Article, id=self.kwargs['pk'])
        total_likes = like_data.total_likes()
        context["total_likes"] = total_likes
        context["country"] = article.country
        context['comment_form'] = forms.CommentCreateForm() # Form to add comments to the article
        return context


def add_comment_to_article(request, article_id):
    # Adds a comment to a specific article
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = forms.CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.name = request.user
            comment.save()
            return redirect('articles:detail', pk=article_id)

    return redirect('articles:detail', pk=article_id)


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


@login_required(login_url="/accounts/signin/")
def article_edit(request, pk):
    # View to handle the editing of an existing article
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', pk=pk)
    else:
        form = forms.CreatePost(instance=article)
    return render(request, 'exchange/article_edit.html', {'form': form, 'article': article})


@login_required(login_url="/accounts/signin/")
def article_delete(request, pk):
    # View to handle the deletion of an article
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    return render(request, 'exchange/article_delete.html', {'article': article})


class CountryListView(ListView):
    # List view to display articles filtered by country and tags
    template_name = 'exchange/countries.html'
    context_object_name = 'countryList'

    def get_queryset(self):
        countryName = self.kwargs['country']
        tags = self.request.GET.getlist('tags')

        if tags:
            posts = Article.objects.filter(country__name=countryName, tags__slug__in=tags).distinct()
        else:
            posts = Article.objects.filter(country__name=countryName)

        return {
            'country': countryName,
            'posts': posts
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # retrieves existing context data from superclass 'ListView'
        context['country_name'] = self.kwargs['country']
        allTags = Tags.objects.all()  # Retrieves all the tags
        interestTags = allTags.filter(name__in=["Food", "Festival", "Culture", "Holidays"])  # Filters the tags based on the names
        travelTypeTags = allTags.filter(name__in=["Solo Travel", "Group Travel", "Adventure Travel", "Roadtrip"])
        context['interest_tags'] = interestTags  # Add'interestTags' queryset to context dictionary under the key 'interest_tags'
        context['travel_type_tags'] = travelTypeTags  # Add'travel_type_tags' queryset to context dictionary under the key 'travelTypeTags'
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context


def country_list(request):
    country_lists = Country.objects.exclude(name='default')
    context = {
        "country_list": country_lists
    }

    return context


class CountryThreadListView(ListView):
    # List view to display threads for a specific country and subcategory
    template_name = 'exchange/country_threads.html'
    context_object_name = 'threads'

    def get_queryset(self):
        countryName = self.kwargs['country']
        subcategory = self.kwargs.get('subcategory', '').lower()
        if subcategory:
            return Thread.objects.filter(country__name=countryName, subcategory=subcategory)
        return Thread.objects.filter(country__name=countryName)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = self.kwargs['country']  # sets current country's name
        context['subcategories'] = [subcat[1] for subcat in Thread.SUBCATEGORY_CHOICES]
        return context


@login_required(login_url="/accounts/signin/")
def add_comment_to_thread(request, thread_id):
    # Adds a comment to a specific thread
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = forms.CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.name = request.user
            comment.save()
            return redirect('articles:thread_detail', pk=thread_id)
    return redirect('articles:thread_detail', pk=thread_id)


class ThreadDetailView(DetailView):
    # Detail view for a specific thread
    model = Thread
    template_name = 'exchange/thread_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadDetailView, self).get_context_data(**kwargs)
        thread = self.get_object()
        context['comment_form'] = forms.CommentCreateForm()  # Ensure this is correctly added
        return context

@login_required(login_url="/accounts/signin/")
# Handles the creation of a new thread for a specified country
def thread_create(request, country):
    if request.method == 'POST':
        form = forms.ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.country = get_object_or_404(Country, name=country)
            thread.author = request.user
            thread.save()
            return redirect(reverse('articles:country_threads', args=[country]))
    else:
        form = forms.ThreadForm()
    return render(request, 'exchange/thread_create.html', {'form': form, 'country': country})


@login_required(login_url="/accounts/signin/")
def thread_edit(request, pk):
    # Handles the editing of an existing thread
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        form = forms.ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('articles:thread_detail', pk=pk)
    else:
        form = forms.ThreadForm(instance=thread)
    return render(request, 'exchange/thread_edit.html', {'form': form, 'thread': thread})


@login_required(login_url="/accounts/signin/")
def thread_delete(request, pk):
    # Handles the deletion of a thread
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        thread.delete()
        return redirect(reverse('articles:country_threads', args=[thread.country.name]))
    return render(request, 'exchange/thread_delete.html', {'thread': thread})


@login_required(login_url="/accounts/signin/")
def like_thread(request, pk):
    # Handles the like functionality for threads
    thread = get_object_or_404(Thread, id=request.POST.get('thread_id'))
    # id is getting the thread_id assigned from the thread_detail html form,
    # retrieving it, and looking in the Thread table
    thread.likes.add(request.user)  # Save the user's like in the database
    return HttpResponseRedirect(reverse('articles:thread_detail', args=[str(pk)]))


