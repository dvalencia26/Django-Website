from django.urls import path, re_path
from exchange import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from.views import ArticleDetailView

app_name = 'articles'

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path('travelPage/', views.article_list, name="travelPage"),
    re_path(r'^create/$', views.article_create, name="create"),
    # re_path(r'^(?P<slug>[\w-]+)/$', views.article_details, name="detail"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="detail"),
    # path('category/<str:cat>/', views.category, name='category'),
    path('like/<int:pk>', views.like, name='like_post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

