from django.views.generic import ListView
from .models import Book


class BookList(ListView):
    template_name = 'book_list.html'
    model = Book
    context_object_name = 'books'
