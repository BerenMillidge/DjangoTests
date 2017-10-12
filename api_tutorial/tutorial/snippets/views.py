from django.shortcuts import render

# Create your views here.

#these are for API views, so we can try to udnerstand what's going on here
#imports:
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import *
from snippets.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
#authentication:
from rest_framework import permissions
from snippets.permissions import *
from rest_framework.reverse import reverse
from rest_framework import renderers

# this is a highlighter, I am kind of lost about how this works. I guess when I start implementing my own, and go through this tutorial agani, it will make signifiacntly more sense - I hope so. I really do hope it's fairly trivial in the end, but  I don't currently really get what's going on!

class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

# our root api endpoint which is defined as a function view and not a class view - I still don't really understnd the difference here!

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})


## our user model api endpoints

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	


#we can also rewrite this all using generic class based views, for ultiamte abstracion, so we can have no real idea what's going on, but it doesn't take much code!

class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	#authentication
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	#this makes sure that the user, which is part of the request, and not the serialized snippet, is added when the snippet is part of the database
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	#authenticated
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

#to be honest, this is so smiple and abstracted, that I don't think using it would be a good idea, as I have no real idea how it works, and this won't build understanding in any serious manner, but just lead to pointless mimicry. I think thec class based functoins are a good intermediate!


#that was the class based view, we can also do it with mixins, which will be even fster andeasier

## I really don't understand mixins. or what they do. this is something I'm going to have to look up, probably later, after we've finished this tutorial

class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *rgs, **kwargs):
		return self.destroy(request, *args, **kwargs)



# we can also refactor our apis to use class-based views instead, which will simplify things further

"""
class SnippetList(APIView):
	#we list all snippets or create a new snippet
	def get(self, request, format=None):
		snippets = Snippet.objects.all();
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = SnippetSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
	def get_object(self, pk):
		try:
			return Snippet.objects.get(pk=pk)
		except Snippet.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = SnippetSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

"""

#the other benefit is we're no longer tied to json. Response can handle other formats, such as XML or whatever

# we can also add format views/suffixes which allow us to handle urls which explicitly refer to a given format i.e. api/items/4.json

