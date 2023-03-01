from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.forms import BaseModelForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponse, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from .models import Book, Review


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'account_login' 
    permission_required = ('books.add_book',)

    model = Book
    template_name = 'books/book_create.html'
    fields = ('title', 'cover', 'author', 'price')

    # def test_func(self) -> bool:
    #     return self.request.user.is_superuser


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'account_login' 
    permission_required = ('books.change_book',)

    model = Book
    template_name = 'books/book_update.html'
    fields = ('title', 'cover', 'author', 'price')

    # def test_func(self) -> bool:
    #     return self.request.user.is_superuser


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'account_login' 
    permission_required = ('books.delete_book',)

    model = Book
    template_name = 'books/book_delete_confirm.html'
    success_url = reverse_lazy('book_list')

    # def test_func(self) -> bool:
    #     return self.request.user.is_superuser


class BookList(LoginRequiredMixin, ListView):
    login_url = 'account_login' 
    template_name = 'books/book_list.html'
    model = Book
    context_object_name = 'books'


class BookDetailed(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = 'account_login' 
    permission_required = ('books.privilegios_group',)

    template_name = 'books/book_detailed.html'
    model = Book


class ReviewCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'account_login' 
    permission_required = ('books.add_review',)

    model = Review
    fields = ('review',)
    template_name = 'books/review_create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        book_id = int(self.kwargs['pk'])
       
        form.instance.book = Book.objects.get(id=book_id)
        return super().form_valid(form)


@permission_required('books.delete_review', raise_exception=True)
@login_required(login_url='account_login')
def delete_review(request, book_uuid, review_id):
    review = Review.objects.get(id=review_id)
    if not request.user.is_superuser and review.author != request.user:
        raise PermissionDenied()

    review.delete()
    return redirect(reverse('book_detailed', args=[str(book_uuid)]))