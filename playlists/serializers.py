from rest_framework import serializers
from .models import Playlist
from songs.models import Song
class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('title', 'content')
        
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = "__all__"

class SongDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("title", "singer", "genre")

class PlaylistDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    playlist_detail = SongDetailSerializer(many=True)
    
    def get_user(self, obj):
        return obj.user.email
    
    # def get_playlist_detail(self, obj):
    #     context = {}
    #     context["title"] = obj.playlist_detail.song.title
    #     context["singer"] = obj.playlist_detail.song.singer
    #     context["genre"] = obj.playlist_detail.song.genre
    #     return context
    
    class Meta:
        model = Playlist
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'playlist_detail','user',)