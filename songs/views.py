from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Song, Comment
from songs.serializers import SongSerializer,CommentSerializer, CommentCreateSerializer
# Create your views here.


class SongView(APIView):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SongLikeView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        if request.user in song.song_likes.all():
            song.song_likes.remove(request.user)
            return Response("좋아요 취소했습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            song.song_likes.add(request.user)
            return Response("좋아요 했습니다.", status=status.HTTP_200_OK)

class SearchView(APIView):
    def get(self, request):
        post_result = Song.object.all()
    pass



class CommentView(APIView):
    
    def get(self, request, song_id):
        song = Song.objects.get(id=song_id)
        comments = song.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, song_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=song_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):

    def put(self, request, song_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_vaild():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, comment_id):
        comment= get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)