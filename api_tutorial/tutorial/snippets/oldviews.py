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

# one simple way to refactor is to use the REST apis response instead of the JSON response

# so, first we are going to create a root API view (waht does this mean?) that supports listing all existing snippets or creating  new snippet

@csrf_exempt	#done as a quick hack. DONT do this in production
def snippet_list(request):
	#list all snippets or create a new snippe
	if request.method == 'GET':
		snippets = Snippet.objects.all() #get all our snippets
		serializer = SnippetSerializer(snippets, many=True)
		return JsonResponse(serializer.data, safe=False)
		#this actually works and makes a whole load of sense. wow. that's not too hard at all!

	elif request.method == 'POST':
		data = JSONParser().parse(request) # we parse request, as we've got stuff incoming
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	#wow, that's not complicated at all. pretty easy and simple and nice yay!

#okay, this is a view corresponding to an individual snippet which can be used to retrieve, update or delete the snippet, I'm not sure how this is meant to work in an API but okay!

@csrf_exempt
def snippet_detail(request, pk):
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)

	#okay, we gget the actual thing
	#now we begin the request properly
	if request.method=='GET':
		serializer =SnippetSerializer(snippet)
		return JsonResponse(serializer.data)
	
	elif request.method=='PUT':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method=='DELETE':
		snippet.delete()
		return HttpResponse(status=204)
		
