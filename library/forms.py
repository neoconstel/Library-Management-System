from django.forms import ModelForm
from .models import Book, User
from django.contrib.auth.forms import UserCreationForm


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']