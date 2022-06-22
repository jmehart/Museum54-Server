"""View module for handling requests about artist types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
import uuid
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from django.contrib.auth.models import User
from app_api.models import Artist, Curator


class ArtistView(ViewSet):
    """Level up artist types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist type
        Returns:
            Response -- JSON serialized artist type
        """
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all artist types
        Returns:
            Response -- JSON serialized list of artist types
        """
        
        name = self.request.query_params.get("name", None)
        
        if name != None:
            artists = Artist.objects.filter(Q(name__contains = name)).order_by('-name')
        else:   
            artists = Artist.objects.all().order_by('name')
        # What if we wanted to pass in a query string parameter?
        # The request from the method parameters holds all the information for the request from the client. The request.query_params is a dictionary of any query parameters that were in the url. Using the .get method on a dictionary is a safe way to find if a key is present on the dictionary. If the 'type' key is not present on the dictionary it will return None.
        serializer = ArtistSerializer(artists, many=True, context={'request': request})
        return Response(serializer.data)

    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized artist instance
        """
        curator = Curator.objects.get(user=request.auth.user)
        
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')
    
        
        artist = Artist()
        
        artist.curator = curator
        artist.name = request.data["name"]
        artist.birth = request.data["birth"]
        artist.death = request.data["death"]
        artist.bio = request.data["bio"]
        artist.nationality = request.data["nationality"]
        artist.dateEntered = request.data["dateEntered"]
        artist.image = data
        

        try:
            artist.save()
            serializer = ArtistSerializer(artist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)   
        

    def update(self, request, pk):
        """Handle PUT requests for a artist
        Returns:
            Response -- Empty body with 204 status code
        """
        
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')

        artist = Artist.objects.get(pk=pk)

        artist.name = request.data["name"]
        artist.birth = request.data["birth"]
        artist.death = request.data["death"]
        artist.bio = request.data["bio"]
        artist.nationality = request.data["nationality"]
        artist.dateEntered = request.data["dateEntered"]
        artist.image = data
        
        artist.save()
    
    
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class ArtistUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

                
class ArtistCuratorSerializer(serializers.ModelSerializer):

    user = ArtistUserSerializer(many=False)
    class Meta:
        model = Curator
        fields = ['id', 'user']
        

# Right now the GET methods do not include any nested data, only the foreign key. Embedding that data is only 1 line of code! Take a look at the response for getting all the artists. Notice that  is just the id of the type. Back in the ArtistSerializer add this to the end of Meta class tabbed to the same level as the fields property
class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artist
    """
    curator = ArtistCuratorSerializer(many=False)
    
    class Meta:
        model = Artist
        fields = ('id', 'name', 'birth', 'death', 'bio', 'nationality', 'curator', 'dateEntered', 'image', 'art')
        depth = 1
        
        
        
# Instead of making a new instance of the Artist model, the request.data dictionary is passed to the new serializer as the data. The keys on the dictionary must match what is in the fields on the serializer. After creating the serializer instance, call is_valid to make sure the client sent valid data. If the code passes validation, then the save method will add the artist to the database and add an id to the serializer.        
        
class CreateArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'birth', 'death', 'bio', 'nationality', 'dateEntered', 'image'] 