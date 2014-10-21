from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    email = models.EmailField()
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=128, unique=True)
    icon = models.ImageField(upload_to='game_icons',blank=True)
    description = models.TextField()
    developer = models.ForeignKey(User)
    picture_1 = models.ImageField(upload_to='game_pictures',blank=True)
    picture_2 = models.ImageField(upload_to='game_pictures',blank=True)
    picture_3 = models.ImageField(upload_to='game_pictures',blank=True)
    link = models.URLField(blank=True)
   
    #created_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title
      
class Comment(models.Model):
  author_alias = models.CharField(max_length=128)
  comment = models.TextField()
  game = models.ForeignKey(Game)
  def __unicode__(self):
    return self.author_alias