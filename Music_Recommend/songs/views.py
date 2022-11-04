from rest_framework import status
from rest_framework.views import APIView
from .models import Song
from rest_framework import permissions
from songs.serializers import SearchSerializer
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.


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

