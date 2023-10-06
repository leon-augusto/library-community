from django.shortcuts import render
from django.http import HttpResponse

from books.forms import BookForm, CategoryForm, BorrowingForm
from books.models import Book, Category
from .models import Client
from django.shortcuts import redirect
from hashlib import sha256


def get_login(request):
    if request.session.get('client'):
        return redirect('/books/home')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def valid_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    password = sha256(password.encode()).hexdigest()

    client = Client.objects.filter(email=email, password=password)

    if len(client) == 0:
        return redirect('/auth/login/?status=1')
    elif len(client) > 0:
        request.session['client'] = client[0].id
        return redirect('/books/home')

    return HttpResponse(f'{email} {password}')


def set_logout(request):
    request.session.flush()
    return redirect('/auth/login/')


def register_client(request):
    if request.session.get('client'):
        return redirect('/books/home')
    status = request.GET.get('status')
    return render(request, 'register.html', {'status': status})


def valid_register(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    client = Client.objects.filter(email=email)

    if len(name.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/register/?status=1')

    if len(password) < 8:
        return redirect('/auth/register/?status=2')

    if len(client) > 0:
        return redirect('/auth/register/?status=3')

    try:
        password = sha256(password.encode()).hexdigest()
        client = Client(name=name, email=email, password=password)
        client.save()

        request.session['client'] = Client.objects.filter(email=email, password=password)[0].id

        return redirect('/books/home/?status=0')
    except:
        return redirect('/auth/register/?status=4')


def get_profile(request):
    client = Client.objects.get(id=request.session['client'])
    form_book, form_category, form_borrowing = BookForm(), CategoryForm(), BorrowingForm()

    form_category.fields['client'].initial = request.session['client']
    form_book.fields['client'].initial = request.session['client']

    form_book.fields['category'].queryset = Category.objects.filter(client=client)
    form_borrowing.fields['book'].queryset = Book.objects.filter(client=client, borrowed=False)
    form_borrowing.fields['responsible'].queryset = Client.objects.all()

    return render(request, 'profile.html', {'client': client,
                                            'client_logged_in': request.session.get('client'),
                                            'form_book': form_book,
                                            'form_category': form_category,
                                            'form_borrowing': form_borrowing})


def upload_photo_user(request):
    photo = request.FILES.get('photo')

    client = Client.objects.get(id=request.session['client'])

    client.photo = photo
    client.save()
    return redirect('/auth/profile/')


def update_name_email(request):
    new_name = request.POST.get('client_name')
    new_email = request.POST.get('client_email')

    client = Client.objects.get(id=request.session['client'])

    if client.name != new_name or client.email != new_email:
        if client.name != new_name:
            client.name = new_name

        if client.email != new_email:
            client.email = new_email

        client.save()

    # else:
        # alert by same datas, no update

    return redirect('/auth/profile/')


def change_password(request):
    new_password = sha256(request.POST.get('client_password').encode()).hexdigest()
    password_again = sha256(request.POST.get('client_password_again').encode()).hexdigest()

    given_password = sha256(request.POST.get('client_current_password').encode()).hexdigest()

    client = Client.objects.get(id=request.session['client'])

    if client.password == given_password:
        if new_password == password_again:
            client.password = new_password
            client.save()
            return redirect('/auth/profile/')
        else:
            return HttpResponse('your passwords are not equals')
    else:
        return HttpResponse('this is not the password')
