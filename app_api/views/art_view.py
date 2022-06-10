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
        style = self.request.query_params.get("style", None)
        title = self.request.query_params.get("title", None)
        

        if user_id != None: 
            art = Art.objects.filter(Q(curator = user_id)).order_by('-title')
        elif artist != None:
            art = Art.objects.filter(Q(artist = artist)).order_by('-title')
        elif classification != None:
            art = Art.objects.filter(Q(classification = classification)).order_by('-title')
        elif style != None:
            art = Art.objects.filter(Q(style = style)).order_by('-title')
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
        
        
        
    def create(self, request):

        user = Curator.objects.get(user=request.auth.user)
        artist = Artist.objects.get(pk=request.data["artist"])

        art = Art()
        
        art.curator = user
        art.title = request.data["title"]
        art.artist = artist
        art.description = request.data["description"]
        art.image = request.data["image"]
        art.dateMade = request.data["dateMade"]
        art.dateAcquired = request.data["dateAcquired"]
        art.dateEntered = request.data["dateEntered"]
        art.location = request.data["location"]
        art.dimensions = request.data["dimensions"]
        art.framed = request.data["framed"]
        art.signature = request.data["signature"]
        

        try:
            art.save()
            art.classification.add(*request.data['classification'])
            art.style.add(*request.data['style'])
            art.genre.add(*request.data['genre'])
            art.medium.add(*request.data['medium'])
            serializer = ArtSerializer(art, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)   
        
        
    def update(self, request, pk=None):

        
        artist = Artist.objects.get(pk=request.data["artist"])

        art = Art.objects.get(pk=pk)

        art.title = request.data["title"]
        art.description = request.data["description"]
        art.artist = artist
        art.image = request.data["image"]
        art.dateMade = request.data["dateMade"]
        art.dateAcquired = request.data["dateAcquired"]
        art.dateEntered = request.data["dateEntered"]
        art.location = request.data["location"]
        art.dimensions = request.data["dimensions"]
        art.framed = request.data["framed"]
        art.signature = request.data["signature"]
        
        art.save()
        art.classification.add(*request.data['classification'])
        art.style.add(*request.data['style'])
        art.genre.add(*request.data['genre'])
        art.medium.add(*request.data['medium'])

        return Response({}, status=status.HTTP_204_NO_CONTENT)     
        
        
    @action(methods=['put'], detail=True)
    def framed(self,request, pk):
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        art.framed = 0
        
    @action(methods=['put'], detail=True)
    def signature(self,request, pk):
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        art.signature = 0
        
        
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
    
    @action(methods=['post', 'delete'], detail=True)
    def style(self, request, pk):
        """Post and Delete requests to add styles to a artwork"""
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        style = request.data['style_id']
        
        if request.method == "POST":
            art.style.add(style)
            response_message = Response({'message': 'Style added'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            art.style.remove(style)
            response_message = Response({'message': 'Style deleted'}, status=status.HTTP_204_NO_CONTENT)
        
        return response_message  
    
    @action(methods=['post', 'delete'], detail=True)
    def genre(self, request, pk):
        """Post and Delete requests to add genres to a artwork"""
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        genre = request.data['genre_id']
        
        if request.method == "POST":
            art.genre.add(genre)
            response_message = Response({'message': 'Genre added'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            art.genre.remove(genre)
            response_message = Response({'message': 'Genre deleted'}, status=status.HTTP_204_NO_CONTENT)
        
        return response_message      
    
    @action(methods=['post', 'delete'], detail=True)
    def medium(self, request, pk):
        """Post and Delete requests to add mediums to a artwork"""
        response_message = ""
        
        art = Art.objects.get(pk=pk)
        medium = request.data['medium_id']
        
        if request.method == "POST":
            art.medium.add(medium)
            response_message = Response({'message': 'Medium added'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            art.medium.remove(medium)
            response_message = Response({'message': 'Medium deleted'}, status=status.HTTP_204_NO_CONTENT)
        
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
        fields = ('id', 'curator', 'title', 'description', 'dateMade', 'artist', 'image', 'dateAcquired', 'dateEntered', 'location', 'dimensions', 'framed', 'signature', 'classification', 'style', 'genre', 'medium' )
        depth = 1