from django.urls import path, re_path
from exchange import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from.views import ArticleDetailView

app_name = 'articles'

urlpatterns = [
    path("", views.index, name="index"),
    # path("home/", views.home, name="home"),
    path('travelPage/', views.article_list, name="travelPage"),  # list all Country-related articles
    re_path(r'^create/$', views.article_create, name="create"),  # url path to create new articles
    # re_path(r'^(?P<slug>[\w-]+)/$', views.article_details, name="detail"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="detail"),  # path for viewing the details of a specific article using a class-based view
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name="thread_detail"),  # path for viewing the detail of a specific thread
    path('like/<int:pk>', views.like, name='like_post'),  # liking a post
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),  # editing an Article
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),  # deleting an Article
    path('article/<int:article_id>/add_comment/', views.add_comment_to_article, name='add_comment_to_article'),  # adding comments to an Article

    #  paths for listing and managing threads related to a specific country
    path('country/<country>', views.CountryListView.as_view(), name="country"),
    path('country/<str:country>/threads/', views.CountryThreadListView.as_view(), name="country_threads"),
    path('country/<str:country>/threads/<str:subcategory>/', views.CountryThreadListView.as_view(), name="country_threads_subcategory"),  # Handling subcategories in Threads

    path('country/<str:country>/thread_create/', views.thread_create, name="thread_create"),  # Create Thread
    path('thread/<int:pk>/like/', views.like_thread, name='like_thread'),  # liking a Thread

    # paths for editing and deleting a thread
    path('thread/<int:pk>/edit/', views.thread_edit, name='thread_edit'),
    path('thread/<int:pk>/delete/', views.thread_delete, name='thread_delete'),
    path('thread/<int:thread_id>/add_comment/', views.add_comment_to_thread, name='add_comment_to_thread'), # adding comments to Thread

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

