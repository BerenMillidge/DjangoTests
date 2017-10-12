#okay, this is where I define the custom permissions we need for the app, which is cool

from rest_framework import permissions

# we define custom permissions as classes, which is weird
class IsOwnerOrReadOnly(permissions.BasePermission):
	#custom permission to only allow owners of an object to edit it

	def has_object_permission(self, request, view, obj):
		#read permissions are allowed to any request,
		if request.method in permissions.SAFE_METHODS:
			return True
		#write permissions are only allowed to owner of the snippet
		return obj.owner == request.user
