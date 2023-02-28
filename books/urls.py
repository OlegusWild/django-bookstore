from django.urls import path
from .views import BookCreate, BookUpdate, BookDelete, BookList, BookDetailed, ReviewCreate, delete_review

urlpatterns = [
    path('', BookList.as_view(), name='book_list'),
    path('add_to_shell/', BookCreate.as_view(), name='add_book'),
    path('<uuid:pk>/delete', BookDelete.as_view(), name='delete_book'),
    path('<uuid:pk>/edit', BookUpdate.as_view(), name='edit_book'),
    path('<uuid:pk>/', BookDetailed.as_view(), name='book_detailed'),

    path('<uuid:pk>/add_review/', ReviewCreate.as_view(), name='add_review'),
    path('<uuid:book_uuid>/reviews/<review_id>/delete/', delete_review, name='delete_review'),
]