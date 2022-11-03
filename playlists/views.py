from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Playlist
from .serializers import PlaylistCreateSerializer, PlaylistSerializer, PlaylistDetailSerializer
# Create your views here.
class PlaylistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        playlist = Playlist.objects.filter(user=request.user.id)
        serializer = PlaylistSerializer(playlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    def post(self, request):
        serializer = PlaylistCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id )
        serializer = PlaylistDetailSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id )
        if request.user == playlist.user:
            serializer = PlaylistCreateSerializer(playlist, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data , status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id )
        if request.user == playlist.user:
            playlist.delete()
            return Response({"message":"삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)
