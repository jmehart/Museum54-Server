"""View module for handling requests about mediums"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Medium

class MediumView(ViewSet):
    """Museum54 app Medium view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single medium
        
        Returns:
            Response -- JSON serialized medium
        """
        
        try:
            medium = Medium.objects.get(pk=pk)
            serializer = MediumSerializer(medium)
            return Response(serializer.data)
        except Medium.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all mediums
        
        Returns:
            Response -- JSON serialized list of mediums
        """
        mediums = Medium.objects.all().order_by('type')
        serializer = MediumSerializer(mediums, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns
            response -- JSON serialized medium instance"""
            
        
        medium = Medium.objects.create(
            type = request.data['type']
        )
        
        serializer = MediumSerializer(medium)
        return Response(serializer.data)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        medium = Medium.objects.get(pk=pk)
        serializer = MediumSerializer(medium, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        medium = Medium.objects.get(pk=pk)
        medium.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class MediumSerializer(serializers.ModelSerializer):
    """JSON serializer for Mediums"""
    class Meta:
        model = Medium
        fields = ('id', 'type')