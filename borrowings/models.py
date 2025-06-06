from django.db import models
from django.conf import settings
from books.models import Book


class Borrowing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        """String representation for Borrowing."""
        return f"{self.user.email} - {self.book.title} ({self.borrow_date})"

    class Meta:
        ordering = ["-borrow_date"]

