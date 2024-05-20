import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# A class needs to be created when working with models
# The class is inheriting some basic functionality that all model will have (models.Model)


class Country(models.Model):
    # Model to represent a country
    name = models.CharField(max_length=100)  # Field to store country name

    def __str__(self):
        # gets the name of the country instead of the object's name
        return self.name


class Comment(models.Model):
    # Model to represent a comment made by a user
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('Article', related_name="comments", on_delete=models.CASCADE, null=True, blank=True)  # Article the comment is related to
    body = models.TextField()
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)  # Unique ID for the comment
    thread = models.ForeignKey('Thread', related_name="comments", on_delete=models.CASCADE, null=True, blank=True) # Thread the comment is related to

    def __str__(self):
        try:
            return f'{self.name.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'


class Profile(models.Model):
    # Model to represent a user's profile
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="exchange/media")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    x_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Tags(models.Model):
    # Model to represent tags that can be added to articles
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True) # Unique slug for the tag

    def __str__(self):
        return self.name


class Article(models.Model):
    # Model to represent an article
    title = models.CharField(max_length=200) # For small to large-sized Strings
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(default='default.png', blank=True)
    # if the related objects should be deleted when the referenced object is deleted, use CASCADE
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    tags = models.ManyToManyField('Tags')

    def total_likes(self):
        # Method to count the total likes for the article
        return self.likes.count()

    def __str__(self):
        return self.title

    def snippet(self):
        # Method to get a short snippet of the article content
        return self.body[:50] + '...'


class Thread(models.Model):
    # Choices for thread subcategories
    SUBCATEGORY_CHOICES = [
        ('lifestyle', 'Lifestyle'),
        ('relationships', 'Relationships'),
        ('stories', 'Stories'),
    ]
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES)
    likes = models.ManyToManyField(User, related_name='thread_likes')

    def __str__(self):
        return f'{self.title} - {self.country.name} ({self.subcategory})'

    def total_likes(self):
        return self.likes.count()

# make migrations files: python manage.py makemigrations
# changes to the database: python manage.py migrate