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

# one simple way to refactor is to use the REST apis response instead of the JSON response

@api_view(['GET', 'POST']) #we use the api view annotator as it's a function view
def snippet_list(request, format=None):
	#list all snippets or create a new snippe
	if request.method == 'GET':
		snippets = Snippet.objects.all() #get all our snippets
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)
		#this actually works and makes a whole load of sense. wow. that's not too hard at all!

	elif request.method == 'POST':
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	#wow, that's not complicated at all. pretty easy and simple and nice yay!

#okay, this is a view corresponding to an individual snippet which can be used to retrieve, update or delete the snippet, I'm not sure how this is meant to work in an API but okay!

#the other benefit is we're no longer tied to json. Response can handle other formats, such as XML or whatever

# we can also add format views/suffixes which allow us to handle urls which explicitly refer to a given format i.e. api/items/4.json

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	#okay, we gget the actual thing
	#now we begin the request properly
	if request.method=='GET':
		serializer =SnippetSerializer(snippet)
		return Response(serializer.data)
	
	elif request.method=='PUT':
		serializer = SnippetSerializer(snippet,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method=='DELETE':
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		
