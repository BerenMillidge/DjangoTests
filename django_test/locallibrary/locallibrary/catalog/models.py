from django.db import models
import uuid  # required for unique book instances

# Create your models here.

class Genre(models.Model):
	# model representing a bok genre

	name = models.CharField(max_length=200, help_text="Enter a book genre")

	def __str__(self):
		# string for representing the mode object
		return self.name

class Book(models.Model):

	#model representing a book (but not a specific copy of a book)

	title = models.CharField(max_length = 200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	#foreign key is used becaues book can only have one author, but authors can have multiple books
	#author is a string rathr than object becaues it hasn't been delared yet
	summary = models.TextField(max_length = 1000, help_text = "Enter a brief descriptionof the book")
	isbn = models.CharField('ISBN', max_length=13, help_text='13 characters')
	genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
	#many to many field as each genre can contain many books. books can cover many genres
	#as genre class alreayd defined we can specify it as an object

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('book-detail', args[str(self.id)])

	#creates a string to define our genre - we use this for the display genre in admin
	def display_genre(self):
		return ', '.join([genre.name for genre in self.genre.all()[:3] ])
	display_genre.short_description= 'Genre'


class BookInstance(models.Model):
	# model representing a specific copy of a book - i.e. that can be borrowed from library
	id = models.UUIDField(primary_key= True, default=uuid.uuid4, help_text="Unique ID for this book")
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length = 200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On Loan'),
		('a', 'Available'),
		('r', 'Reserved'),
		)

	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

	class Meta:
		ordering = ["due_back"]
	

	def __str__(self):
		return '%s (%s)' %(self.id, self.book.title)
	


class Author(models.Model):
	# model representing an author
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length= 100)
	date_of_birth=models.DateField(null=True, blank=True)
	date_of_death= models.DateField('Died', null=True, blank=True)
	
	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	
	def __str__(self):
		return '%s, %s' % (self.last_name, self.first_name)

