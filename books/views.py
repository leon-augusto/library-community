from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from books.models import Book, Category, Borrowing
from clients.models import Client
from .forms import BookForm, CategoryForm, BorrowingForm
from datetime import datetime


def get_home(request):
    if request.session.get('client'):
        client = Client.objects.get(id=request.session['client'])
        books = Book.objects.filter(client=client)

        form_book, form_category, form_borrowing = BookForm(), CategoryForm(), BorrowingForm()

        form_category.fields['client'].initial = request.session['client']
        form_book.fields['client'].initial = request.session['client']

        form_book.fields['category'].queryset = Category.objects.filter(client=client)
        form_borrowing.fields['book'].queryset = Book.objects.filter(client=client, borrowed=False)
        form_borrowing.fields['responsible'].queryset = Client.objects.all()

        borrowed_books = Book.objects.filter(client=client, borrowed=True)

        return render(request, 'home.html', {'books': reversed(books),
                                             'books_tot': len(books),
                                             'client': client,
                                             'client_logged_in': request.session.get('client'),
                                             'form_book': form_book,
                                             'form_category': form_category,
                                             'form_borrowing': form_borrowing,
                                             'borrowed_books': borrowed_books,
                                             'status': request.GET.get('status') if request.GET.get('status') else False})
    else:
        return redirect('/auth/login/?status=2')


def get_book(request, id):
    if request.session.get('client'):
        client = Client.objects.get(id=request.session['client'])
        book = Book.objects.get(id=id)

        form_book, form_category, form_borrowing = BookForm(), CategoryForm(), BorrowingForm()

        form_category.fields['client'].initial = request.session['client']
        form_book.fields['client'].initial = request.session['client']

        form_book.fields['category'].queryset = Category.objects.filter(client=client)
        form_borrowing.fields['book'].queryset = Book.objects.filter(client=client, borrowed=False)
        form_borrowing.fields['responsible'].queryset = Client.objects.all()

        borrowed_books = Book.objects.filter(client=client, borrowed=True)

        if request.session.get('client') == book.client.id:
            books_categories = Category.objects.filter(client_id=request.session.get('client'))
            borrowings = Borrowing.objects.filter(book=book)
            return render(request, 'book.html', {'book': book,
                                                 'books_tot': len(Book.objects.filter(client=client)),
                                                 'client': client,
                                                 'books_categories': reversed(books_categories),
                                                 'borrowings': reversed(borrowings),
                                                 'client_logged_in': request.session.get('client'),
                                                 'form_book': form_book,
                                                 'form_category': form_category,
                                                 'form_borrowing': form_borrowing,
                                                 'borrowed_books': borrowed_books,
                                                 'book_id': id})
        else:
            return HttpResponse('This book is not your!')
    return redirect('/auth/login/?status=2')


def register_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/books/home')
        else:
            return HttpResponse('Invalid Datas')


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/books/home')
        else:
            return HttpResponse('Invalid Datas')


def create_borrowing(request):
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        borrowed_book_id = request.POST.get('book')

        if form.is_valid():
            form.save()

            book = Book.objects.get(id=borrowed_book_id)
            book.borrowed = True
            book.save()
            return redirect('/books/home')
        else:
            return HttpResponse('Invalid Datas')


def return_of_book(request):
    id = request.POST.get('book_id')
    book = Book.objects.get(id=id)
    borrowing = Borrowing.objects.get(Q(book=book) & Q(book_return=None))

    if book and borrowing:
        if borrowing.book.client.id == request.session['client']:
            book.borrowed = False
            book.save()

            borrowing.book_return = datetime.now()
            borrowing.save()
            return redirect('/books/home')
        else:
            return redirect('/books/home')
    else:
        return redirect('/books/home')


def remove_book(request, id):
    book = get_object_or_404(Book, pk=id)
    if book.client.id == request.session['client']:
        book.delete()
        return redirect('/books/home')
    else:
        return redirect('/books/home')


def alter_book(request, id):
    client_categories = Category.objects.filter(client_id=request.session.get('client'))

    book_name = request.POST.get('book_name')
    book_auth = request.POST.get('book_auth')
    book_cd_auth = request.POST.get('book_cd_auth')
    book_category = Category.objects.get(id=request.POST.get('book_category'))

    book = Book.objects.get(id=id)
    if book.client.id == request.session['client'] and book_category in client_categories:
        book.name = book_name
        book.auth = book_auth
        book.cd_auth = book_cd_auth
        book.category = book_category
        book.save()
        return redirect(f'/books/book/{id}')
    else:
        return HttpResponse('error')


def list_borrowings(request):
    client = Client.objects.get(id=request.session['client'])
    borrowings = Borrowing.objects.filter(responsible=client)

    form_book, form_category, form_borrowing = BookForm(), CategoryForm(), BorrowingForm()

    form_category.fields['client'].initial = request.session['client']
    form_book.fields['client'].initial = request.session['client']

    form_book.fields['category'].queryset = Category.objects.filter(client=client)
    form_borrowing.fields['book'].queryset = Book.objects.filter(client=client, borrowed=False)
    form_borrowing.fields['responsible'].queryset = Client.objects.all()

    return render(request, 'borrowings.html', {'client_logged_in': request.session.get('client'),
                                               'borrowings': reversed(borrowings),
                                               'books_tot': len(Book.objects.filter(client=client)),
                                               'form_book': form_book,
                                               'form_category': form_category,
                                               'form_borrowing': form_borrowing,
                                               'client': client})


def process_ava(request):
    book_id = request.POST.get('book_id')
    options = request.POST.get('options')
    borrowing_id = request.POST.get('borrowing_id')

    borrowing = Borrowing.objects.get(id=borrowing_id)

    if borrowing.book.client.id == request.session.get('client'):
        borrowing.available = options
        borrowing.save()
        return redirect(f'/books/book/{book_id}')
    else:
        return HttpResponse(f'This borrowing is not your.')
