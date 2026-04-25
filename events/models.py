from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='🎭')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price_general = models.DecimalField(max_digits=10, decimal_places=2)
    price_vip = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_platinum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name

    def is_upcoming(self):
        return self.date > timezone.now()

    def availability_percent(self):
        if self.total_seats == 0:
            return 0
        return int((self.available_seats / self.total_seats) * 100)

    def book_seats(self, count):
        if self.available_seats >= count:
            self.available_seats -= count
            self.save()
            return True
        raise ValueError("Not enough seats available")

    def release_seats(self, count):
        self.available_seats = min(self.total_seats, self.available_seats + count)
        self.save()
