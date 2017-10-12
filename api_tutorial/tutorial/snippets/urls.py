# so this is where we wire up our api urls. hopefully seeing this will help me understand how this bit works a bit more!

from django.conf.urls import url
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = [
	#url(r'^snippets/$', views.snippet_list),
	#url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),

	#this has changed now we're using class-based-views
	url(r'^snippets/$', views.SnippetList.as_view()),
	url(r'^snippets/(?P<pk>[0-9]+)$', views.SnippetDetail.as_view()),
	#okay, user api endpoints
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

	#for api root
	url(r'^$', views.api_root),
	#for snippet highlights - I'm not sure what thi seven means!
	url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
]

#for the default api endpoints urls
urlpatterns += [
	url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
]

#this adds format suffix patterns to our api patterns here which should be okay
urlpatterns = format_suffix_patterns(urlpatterns)

