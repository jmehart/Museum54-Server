"""View module for handling requests about classifications"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Classification

class ClassificationView(ViewSet):
    """Museum54 app Classification view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single classification
        
        Returns:
            Response -- JSON serialized classification
        """
        
        try:
            classification = Classification.objects.get(pk=pk)
            serializer = ClassificationSerializer(classification)
            return Response(serializer.data)
        except Classification.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all classifications
        
        Returns:
            Response -- JSON serialized list of classifications
        """
        classifications = Classification.objects.all().order_by('type')
        serializer = ClassificationSerializer(classifications, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns
            response -- JSON serialized classification instance"""
            
        
        classification = Classification.objects.create(
            type = request.data['type']
        )
        
        serializer = ClassificationSerializer(classification)
        return Response(serializer.data)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        classification = Classification.objects.get(pk=pk)
        serializer = ClassificationSerializer(classification, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        classification = Classification.objects.get(pk=pk)
        classification.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class ClassificationSerializer(serializers.ModelSerializer):
    """JSON serializer for Classifications"""
    class Meta:
        model = Classification
        fields = ('id', 'type')