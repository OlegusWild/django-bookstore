import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='covers/', blank=True)

    def get_absolute_url(self):
        return reverse('book_detailed', args=[str(self.id)])

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,
        related_name='reviews'  # to reference in tmpls
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    review = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('book_detailed', args=[str(self.book.id)])

    def __str__(self) -> str:
        return self.review
