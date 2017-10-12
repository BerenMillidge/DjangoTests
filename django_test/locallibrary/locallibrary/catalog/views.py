from django.shortcuts import render
from .models import *
from django.views import generic

# Create your views here.

def index(request):
	#view function for homepage of site
	
	#we genereate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	#available books
	num_instances_available = BookInstance.objects.filter(status='a').count()
	num_authors = Author.objects.count() # all is apparently implied by default?

	#get num visits by session
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits +1


	#we render the html template index with the data in the context variable
	return render(
		request, 'index.html',
 context={'num_books': num_books, 
'num_instances': num_instances, 'num_instances_available':num_instances_available,
'num_authors':num_authors, 'num_visits':num_visits}) # appeneded num visits





class BookListView(generic.ListView):
	model = Book
	#context_object_name = 'my_book_lis' # your own name for the list
	#queryset = Book.objects.filer(title_icontains='war')[:5] # customised query
	#template_name = 'books/my_arbitrary_template_name_list.html'# overwrite the default expected save location
	paginate_by = 15



#detail view class, to make this very easy also!
class BookDetailView(generic.DetailView):
	model = Book


