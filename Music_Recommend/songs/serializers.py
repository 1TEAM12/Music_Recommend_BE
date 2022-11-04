from rest_framework import serializers
from songs.models import Song

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("title","genre","singer","image")