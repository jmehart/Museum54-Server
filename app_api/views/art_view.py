from urllib import response
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.functions import Coalesce
from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from rest_framework.decorators import action
from app_api.models import Art, Curator, Artist

class ArtView(ViewSet):
    
    def list(self, request):

        user_id = self.request.query_params.get("user_id", None)
        artist = self.request.query_params.get("artist", None)
        classification = self.request.query_params.get("classification", None)
        title = self.request.query_params.get("title", None)
        

        if user_id != None: 
            art = Art.objects.filter(Q(curator = user_id)).order_by('-title')
        elif artist != None:
            art = Art.objects.filter(Q(artist = artist)).order_by('-title')
        elif classification != None:
            art = Art.objects.filter(Q(classification = classification)).order_by('-title')
        elif title != None:
            art = Art.objects.filter(Q(title__contains = title)).order_by('-title')
        else:   
            art = Art.objects.all().order_by('title')

        
        serializer = ArtSerializer(
            art, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):

        try:
            art = Art.objects.get(pk=pk)
            serializer = ArtSerializer(art, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk):
        art = Art.objects.get(pk=pk)
        art.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
        
    # def create(self, request):

    #     user = Curator.objects.get(user=request.auth.user)
    #     artist = Artist.objects.get(pk=request.data["artist"])

    #     art = Art()
    #     art.curator = user
    #     art.title = request.data["title"]
    #     art.artist = artist
    #     art.content = request.data["content"]
    #     art.image_url = request.data["image_url"]
    #     art.approved = request.data["approved"]
        

    #     try:
    #         art.save()
    #         art.classifications.add(*request.data['classifications'])
    #         serializer = ArtSerializer(art, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except ValidationError as ex:
    #         return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)   
        
        
    # def update(self, request, pk=None):

        
    #     artist = Artist.objects.get(pk=request.data["artist"])

    #     art = Art.objects.get(pk=pk)
    #     # art.curator = request.data['curator']
    #     art.title = request.data["title"]
    #     art.content = request.data["content"]
    #     art.artist = artist
    #     art.image_url = request.data["image_url"]
    #     art.approved = request.data["approved"]
    #     art.save()
    #     art.classifications.add(*request.data['classifications'])

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)     
        
        
    @action(methods=['put'], detail=True)
    def approve(self,request, pk):
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        art.approved = 1
        
        
        
        
    @action(methods=['post', 'delete'], detail=True)
    def classification(self, request, pk):
        """Post and Delete requests to add classifications to a artwork"""
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        classification = request.data['classification_id']
        
        if request.method == "POST":
            art.classification.add(classification)
            response_message = Response({'message': 'Classification added'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            art.classification.remove(classification)
            response_message = Response({'message': 'Classification deleted'}, status=status.HTTP_204_NO_CONTENT)
        
        return response_message

class ArtUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ArtCuratorSerializer(serializers.ModelSerializer):

    user = ArtUserSerializer(many=False)
    
    class Meta:
        model = Curator
        fields = ['id', 'user']
        

class ArtistSerializer(serializers.ModelSerializer):
    
    curator = ArtCuratorSerializer(many=False)
    
    class Meta:
        model = Artist
        fields = ('id', 'name', 'birth', 'death', 'bio', 'nationality', 'dateEntered', 'curator', 'image')    
        
        
class ArtSerializer(serializers.ModelSerializer):
    
    curator = ArtCuratorSerializer(many=False)
    artist = ArtistSerializer(many=False)

    class Meta:
        model = Art
        fields = ('id', 'curator', 'title', 'description', 'dateMade', 'artist', 'image', 'dateAcquired', 'dateEntered', 'location', 'dimensions', 'framed', 'signature', 'classification' )
        depth = 1