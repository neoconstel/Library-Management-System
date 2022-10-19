from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (View, TemplateView, CreateView, ListView,
DetailView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from requests import request
from django.db.models import Q  # for combining filter queries with &, |
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .models import Book, Order, Student
from .forms import BookForm, UserSignupForm


class Home(TemplateView):
    template_name = 'library/index.html'


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('admin-portal')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_mode'] = 'Add'
        return context


class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    fields = '__all__'
    context_object_name = 'book'


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'    

    def get_success_url(self) -> str:
        return reverse_lazy('view-books', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_mode'] = 'Update'
        return context


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('admin-portal')



class AdminPortal(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'library/admin_library.html'
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


class StudentPortal(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'library/student_portal.html'
    context_object_name = 'orders'
    ordering = ['-id']    


class ViewOrders(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = 'order'
    success_url = reverse_lazy('student-portal')


class OrderCreate(LoginRequiredMixin, View):

    def post(request, *args, **kwargs):    
        book_id = request.request.POST.get('book_id')
        student_id = request.request.POST.get('student_id')
        new_order = Order(
            book = Book.objects.get(id=book_id),
            student = Student.objects.get(id=student_id)
        )
        new_order.save()

        # redirect back to page that made initial request
        return HttpResponseRedirect(request.request.META.get('HTTP_REFERER'))


class StudentLibrary(AdminPortal):
    template_name = 'library/student_library.html'


class LoginRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        if self.request.user.is_staff:
            return redirect(reverse_lazy('admin-portal'))
        else:
            return redirect(reverse_lazy('student-portal'))


class SignupView(LoginRequiredMixin, View):

    def get(self, request):
        form = UserSignupForm()

        context = {
            'form': form
        }
        return render(request, 'registration/signup.html', context=context)

    
    def post(self, request):
        form = UserSignupForm(self.request.POST)

        if form.is_valid():
            form.save()
            
            # new user has been added. Create a student instance and assign new user to it
            newest_user = User.objects.last()
            new_student = Student(name=newest_user.username, user=newest_user)
            new_student.save()
        
            return redirect('login')
        
        return redirect('.')