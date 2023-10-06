from django import forms
from .models import Book, Category, Borrowing


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['img'].widget = forms.FileInput(attrs={'class': 'form-control-file'})
        self.fields['auth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['cd_auth'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['category'].widget = forms.Select(attrs={'class': 'form-control'})

        self.fields['register_date'].widget = forms.HiddenInput()
        self.fields['borrowed'].widget = forms.HiddenInput()
        self.fields['client'].widget = forms.HiddenInput()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})

        self.fields['client'].widget = forms.HiddenInput()


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['responsible'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['anonymous_responsible'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['borrowing_date'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['book'].widget = forms.Select(attrs={'class': 'form-control'})

        self.fields['book_return'].widget = forms.HiddenInput()
        self.fields['available'].widget = forms.HiddenInput()
