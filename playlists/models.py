from django.db import models
from users.models import User
from songs.models import Song
# Create your models here.
class Playlist(models.Model):
    title = models.CharField(max_length=50, blank=True)
    content = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_detail = models.ManyToManyField(Song, related_name='playlist_detail')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']    
    