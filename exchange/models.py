from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# A class needs to be created when working with models
# The class is inheriting some basic functionality that all model will have (models.Model)

# class Category(models.Model):
#    name = models.CharField(max_length=200)

#    def __str__(self):
#        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="exchange/media")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    x_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)



    def __str__(self):
        return str(self.user)


class Article(models.Model):
    title = models.CharField(max_length=200) # For small to large-sized Strings
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(default='default.png', blank=True)
    # if the related objects should be deleted when the referenced object is deleted, use CASCADE
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    # category = models.CharField(max_length=255, default=None)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    # Add Tags functionality
    # Use true or false to display tag
    # def total_likes(self):
    #    return self.likes.count()

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50] + '...'


# make migrations files: python manage.py makemigrations
# changes to the database: python manage.py migrate