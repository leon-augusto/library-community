from django.contrib import admin
from .models import Book, Category, Borrowing

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Borrowing)
