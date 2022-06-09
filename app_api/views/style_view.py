"""View module for handling requests about styles"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Style

class StyleView(ViewSet):
    """Museum54 app Style view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single style
        
        Returns:
            Response -- JSON serialized style
        """
        
        try:
            style = Style.objects.get(pk=pk)
            serializer = StyleSerializer(style)
            return Response(serializer.data)
        except Style.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all styles
        
        Returns:
            Response -- JSON serialized list of styles
        """
        styles = Style.objects.all().order_by('type')
        serializer = StyleSerializer(styles, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns
            response -- JSON serialized style instance"""
            
        
        style = Style.objects.create(
            type = request.data['type']
        )
        
        serializer = StyleSerializer(style)
        return Response(serializer.data)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        style = Style.objects.get(pk=pk)
        serializer = StyleSerializer(style, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        style = Style.objects.get(pk=pk)
        style.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class StyleSerializer(serializers.ModelSerializer):
    """JSON serializer for Styles"""
    class Meta:
        model = Style
        fields = ('id', 'type')