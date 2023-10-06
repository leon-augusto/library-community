from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.get_home, name='home'),
    path('book/<int:id>', views.get_book, name='book'),
    path('register_book/', views.register_book, name='register_book'),
    path('create_category/', views.create_category, name='create_category'),
    path('create_borrowing/', views.create_borrowing, name='create_borrowing'),
    path('return_of_book/', views.return_of_book, name='return_of_book'),
    path('remove_book/<int:id>', views.remove_book, name='remove_book'),
    path('alter_book/<int:id>', views.alter_book, name='alter_book'),
    path('borrowings/', views.list_borrowings, name='borrowings'),
    path('process_ava/', views.process_ava, name='process_ava'),
]
