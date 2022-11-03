from django.db import models
from users.models import User

# Create your models here.

class Song(models.Model):
    year = models.CharField(max_length=70, blank=True)
    rank = models.CharField(max_length=70, blank=True)
    title = models.CharField(max_length=70, blank=True)
    genre = models.CharField(max_length=70, blank=True)
    singer = models.CharField(max_length=70, blank=True)
    type = models.CharField(max_length=70, blank=True)
    lyrics = models.TextField(blank=True)
    likes = models.IntegerField(blank=True)
    image = models.TextField(blank=True)
    genre_no = models.IntegerField(blank=True)
    song_likes = models.ManyToManyField(User, related_name="like_song")
    
    class Meta: 
        db_table = 'song'
        ordering = ['id']

    def __str__(self):
        return str(self.title) 


class Voice(models.Model):
    # recode = models.File
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    voice_likes = models.ManyToManyField(User, related_name="like_voice")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    class Meta:
        db_table = 'voice'
        ordering = ['-created_at']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    content= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.content)

