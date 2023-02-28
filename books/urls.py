from django.urls import path
from .views import BookList, BookDetailed

urlpatterns = [
    path('', BookList.as_view(), name='book_list'),
    path('<uuid:pk>/', BookDetailed.as_view(), name='book_detailed'),
]