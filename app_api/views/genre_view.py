"""View module for handling requests about genres"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Genre

class GenreView(ViewSet):
    """Museum54 app Genre view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single genre
        
        Returns:
            Response -- JSON serialized genre
        """
        
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all genres
        
        Returns:
            Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all().order_by('type')
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns
            response -- JSON serialized genre instance"""
            
        
        genre = Genre.objects.create(
            type = request.data['type']
        )
        
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for Genres"""
    class Meta:
        model = Genre
        fields = ('id', 'type')