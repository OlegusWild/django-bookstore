from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms import BaseModelForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponse, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Book, Review


class BookCreate(UserPassesTestMixin, CreateView):
    model = Book
    template_name = 'books/book_create.html'
    fields = ('title', 'cover', 'author', 'price')

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class BookUpdate(UserPassesTestMixin, UpdateView):
    model = Book
    template_name = 'books/book_update.html'
    fields = ('title', 'cover', 'author', 'price')

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class BookDelete(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_delete_confirm.html'
    success_url = reverse_lazy('book_list')

    def test_func(self) -> bool:
        return self.request.user.is_superuser


class BookList(ListView):
    template_name = 'books/book_list.html'
    model = Book
    context_object_name = 'books'


class BookDetailed(DetailView):
    template_name = 'books/book_detailed.html'
    model = Book


class ReviewCreate(CreateView):
    model = Review
    fields = ('review',)
    template_name = 'books/review_create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        book_id = int(self.kwargs['pk'])
       
        form.instance.book = Book.objects.get(id=book_id)
        return super().form_valid(form)


def delete_review(request, book_uuid, review_id):
    review = Review.objects.get(id=review_id)
    if not request.user.is_superuser and review.author != request.user:
        raise PermissionDenied()

    review.delete()
    return redirect(reverse('book_detailed', args=[str(book_uuid)]))