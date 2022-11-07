from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .pagination import PaginationHandlerMixin
from .models import Song, Voice, Comment
from songs.serializers import (SongSerializer, VoiceCreateSerializer, 
VoiceSerializer, CommentSerializer, CommentCreateSerializer, SearchSerializer)

from rest_framework.pagination import PageNumberPagination

#Comment, Voice 페이지네이션
class CommetVoicePagination(PageNumberPagination):
    page_size = 10

#Serach 페이지네이션
class SearchPagination(PageNumberPagination):
    page_size = 8
    
######Song######
class SongView(APIView):
    permission_classes = [IsAuthenticated]
    
    #음악 상세페이지
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

#노래 좋아요
class SongLikeView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        if request.user in song.song_likes.all():
            song.song_likes.remove(request.user)
            return Response("좋아요 취소.", status=status.HTTP_200_OK)
        else:
            song.song_likes.add(request.user)
            return Response("좋아요 함.", status=status.HTTP_200_OK)

#노래 검색
# class SearchView(PaginationHandlerMixin, APIView):
#     pagination_class = SearchPagination
#     # permission_classes = [IsAuthenticated] 
    
#     def get(self, request):
#         keyword = request.GET.get('keyword')
#         if keyword =='':
#             return Response("검색 결과가 없습니다.", status=status.HTTP_200_OK)
        
#         post_result = Song.objects.filter(
#         Q(title__icontains=keyword) |
#         Q(singer__icontains=keyword)|
#         Q(genre__icontains=keyword)
#         )
#         page = self.paginate_queryset(post_result)
#         serializer = self.get_paginated_response(SearchSerializer(page,many=True).data)
    
#       return Response(serializer.data, status=status.HTTP_200_OK)

class SearchView(APIView):
# permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
    # post_result = Song.objects.all()
        keyword = request.GET.get('keyword')
        if keyword:
            post_result = Song.objects.filter(
            Q(title__icontains=keyword) |
            Q(singer__icontains=keyword)|
            Q(genre__icontains=keyword)
            )
        serializer = SearchSerializer(post_result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


######Voice######
class VoiceView(PaginationHandlerMixin, APIView):
    pagination_class = CommetVoicePagination
    permission_classes = [IsAuthenticated]

    #모창 전체 리스트
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        voice = song.voices.all()
        page = self.paginate_queryset(voice)
        serializer = self.get_paginated_response(VoiceSerializer(page,many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #모창 생성
    def post(self, request, song_id):
        serializer = VoiceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, song_id=song_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VoiceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    #모창 수정
    def put(self, request, song_id, voice_id):
        voice = get_object_or_404(Voice, id=voice_id)
        if request.user == voice.user:
            serializer = VoiceCreateSerializer(voice, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, song_id=song_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("접근 권한 없음", status=status.HTTP_403_FORBIDDEN)
    
    #모창 삭제
    def delete(self, request, song_id, voice_id):
        voice = get_object_or_404(Voice, id=voice_id)
        if request.user == voice.user:
            voice.delete()
            return Response(status=status.HTTP_200_OK)
        return Response("접근 권한 없음", status=status.HTTP_403_FORBIDDEN)
    
#모창 좋아요
class VoiceLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, voice_id):
        voice = get_object_or_404(Voice, id=voice_id)
        if request.user in voice.voice_likes.all():
            voice.voice_likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            voice.voice_likes.add(request.user)
            return Response("좋아요 함", status=status.HTTP_200_OK)

######Comment######
class CommentView(PaginationHandlerMixin, APIView):
    pagination_class = CommetVoicePagination
    permission_classes = [IsAuthenticated] 
    
    #댓글 전체 리스트
    def get(self, request, song_id):
        song = Song.objects.get(id=song_id)
        comments = song.comments.all()
        page = self.paginate_queryset(comments)
        serializer = self.get_paginated_response(CommentSerializer(page,many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #댓글 생성
    def post(self, request, song_id):
        print(request.data)
        serializer = CommentCreateSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=request.user, song_id=song_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    
    #댓글 수정
    def put(self, request, song_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, song_id=song_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("접근 권한 없음", status=status.HTTP_403_FORBIDDEN)

    #댓글 삭제
    def delete(self, request, song_id, comment_id):
        comment= get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        return Response("접근 권한 없음", status=status.HTTP_403_FORBIDDEN)

