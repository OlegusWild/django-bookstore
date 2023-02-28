from django.views.generic import ListView, DetailView
from .models import Book


class BookList(ListView):
    template_name = 'books/book_list.html'
    model = Book
    context_object_name = 'books'

class BookDetailed(DetailView):
    template_name = 'books/book_detailed.html'
    model = Book
