# okay, this is aour serialiser object which works to turn our objects into and out of json, and other formats as desired. so django has things to do this for you, which is immensely nice, so let's work t this!

from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


# our user serialiser, so we can add representatiosn of these to our api

class UserSerializer(serializers.ModelSerializer):
	snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

	class Meta:
		model = User
		fields = ('id', 'username', 'snippets')


#to make things easier we can also just do our serialiser as a model serializer - i.e.
class SnippetSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Snippet
		fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')

# these aren't magical, they just repeat the above one with the default fields set up and the standard default implementatoins of create and update -if we want to customise, we'll have to roll our own, so knowing how to do that is important


"""#the main deal
class SnippetSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
	code = serializers.CharField(style={'base_template': 'textarea.html'})
	linenos = serializers.BooleanField(required=False)
	language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default = 'python')
	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

	#create and return a new snippet instance given validated data
	def create(self, validated_data):
		return Snippet.objects.create(**validated_data)

	def update(self, instance, validated_data):
		#update the instance and return the existing snippet instance given thevaliadted data
	
		instance.title = validated_data.get('title', instance.title)
		instance.code = validated_data.get('code', instance.code)
		instance.linenos = validated_data.get('linenos', instance.linenos)
		instance.language = validated_data.get('language', instance.language)
		instance.style= validated_data.get('style', instance.style)
		instance.save()
		return instance

"""






























