from django.db import models
from datetime import date, datetime
from clients.models import Client


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categorie'


class Book(models.Model):
    img = models.ImageField(upload_to='capa')
    name = models.CharField(max_length=100)
    auth = models.CharField(max_length=30)
    cd_auth = models.CharField(max_length=30, blank=True, null=True)
    register_date = models.DateField(default=date.today)
    borrowed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Borrowing(models.Model):
    choices = (
        ('B', 'Bad'),
        ('R', 'Regular'),
        ('G', 'Good'),
        ('A', 'Awesome')
    )
    responsible = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    anonymous_responsible = models.CharField(max_length=30, blank=True, null=True)
    borrowing_date = models.DateTimeField(default=datetime.now())
    book_return = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    available = models.CharField(max_length=1, choices=choices, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.responsible} | {self.book}'
