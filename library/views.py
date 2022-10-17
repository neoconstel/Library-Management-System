from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (TemplateView, CreateView, ListView,
DetailView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from requests import request
from django.db.models import Q  # for combining filter queries with &, |

from .models import Book, Order
from .forms import BookForm


class Home(TemplateView):
    template_name = 'library/index.html'


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('admin-portal')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_mode'] = 'Add'
        return context


class BookDetail(DetailView):
    model = Book
    fields = '__all__'
    context_object_name = 'book'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'    

    def get_success_url(self) -> str:
        return reverse_lazy('view-books', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_mode'] = 'Update'
        return context


class BookDelete(DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('admin-portal')



class AdminPortal(ListView):
    model = Book
    template_name = 'library/admin_portal.html'
    context_object_name = 'books'
    ordering = '-id'


    def get_queryset(self):
        # get the search term from a form in the template, submitted with GET method
        search_term = self.request.GET.get('search_field')

        if search_term:
            # filter example format: <model field>__icontains=<search term>
            filtered_query = self.model.objects.filter(
                Q(author__istartswith=search_term) 
                | Q(title__icontains=search_term)
                | Q(id__iexact=search_term)
                ).order_by(self.ordering).all()
            return filtered_query
        else:
            # return this query if search field is empty (e.g on page load)
            return self.model.objects.order_by(self.ordering).all()  # or None, depending on preference


    def get_context_data(self, **kwargs):
        # get the default data for editing
        context = super().get_context_data(**kwargs)

        # fetch our data and include it in default data
        books = Book.objects.all()     
        context['total_book_titles'] = books.count()
        context['books_rented_out'] = Order.objects.count()
        context['total_available_books'] = sum([book.quantity for book in books])

        # return the modified data
        return context


class StudentPortal(ListView):
    model = Book
    template_name = 'library/student_portal.html'
    context_object_name = 'books'
    ordering = ['-id']


class ViewOrders(ListView):
    model = Order
    context_object_name = 'orders'



