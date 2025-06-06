from django.db import models
from django.core.validators import MinValueValidator


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hard"
        SOFT = "SOFT", "Soft"

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    cover = models.CharField(
        max_length=4,
        choices=CoverType.choices,
        default=CoverType.HARD
    )
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.0)]
    )

    def __str__(self) -> str:
        """Return string representation of a Book."""
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ["title"]


