from django.db import models
from django.urls import reverse
from django.conf.global_settings import LANGUAGES as py_languages
import uuid  # for creating unique key

# Create your models here.


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Romance")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    # a book can have only one author, authors can have multiple books
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book.')
    isbn = models.CharField("ISBN", max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # a genre can contain many books, books can cover many genres.
    genres = models.ManyToManyField(
        "Genre", help_text="Select a genre for this book.")
    language = models.ForeignKey(
        'Language', null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a sepectific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library.")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', "Maintenance"),
        ("o", "On loan"),
        ("a", "Avaiable"),
        ("r", "Reserved")
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default="m", help_text="Book avaiability.")

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    name = models.CharField(max_length=10, null=True,
                            blank=False, choices=py_languages)
