from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (View, TemplateView, CreateView, ListView,
DetailView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from requests import request
from django.db.models import Q  # for combining filter queries with &, |
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .models import Book, Order, Student
from .forms import BookForm, UserSignupForm
from django.contrib.auth.models import Group

# permission -- with object-level support
from rules.contrib.views import PermissionRequiredMixin


class Home(TemplateView):
    template_name = 'library/index.html'


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('admin-library')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form_mode'] = 'Add'
        return context


class BookDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Book
    fields = '__all__'
    context_object_name = 'book'

    permission_required = 'library.read_book'


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
    success_url = reverse_lazy('admin-library')


class Library(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'library/admin_library.html'
    context_object_name = 'books'
    ordering = '-id'
    permission_required = 'auth.is_librarian'


    def get_queryset(self):
        # get the search term from a form in the template, submitted with GET method
        search_term = self.request.GET.get('search_field')

        user = self.request.user

        # query from all books
        query = self.model.objects

        if not user.is_staff:
            student = Student.objects.get(user=user)
            student_orders = Order.objects.filter(student=student)
            student_rented_book_ids = (order.book.id for order in student_orders)
            available_books = query.filter(quantity__gt=0) # quantity > 0
            student_unrented_books = available_books.filter(
                                ~Q(id__in=student_rented_book_ids))

            # query from only AVAILABLE books which are not rented by this student
            query = student_unrented_books

        if search_term:
            # filter example format: <model field>__icontains=<search term>
            filtered_query = query.filter(
                Q(author__icontains=search_term) 
                | Q(title__icontains=search_term)
                | Q(id__iexact=search_term)
                | Q(theme__icontains=search_term)
                ).order_by(self.ordering).all()
            return filtered_query
        else:
            # return this query if search field is empty (e.g on page load)
            return query.order_by(self.ordering).all()


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


class StudentCollections(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'library/student_portal.html'
    context_object_name = 'orders'
    ordering = ['-id']



class ViewOrders(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'


class OrderDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = 'order'
    success_url = reverse_lazy('student-collections')

    permission_required = 'library.delete_order'


class OrderCreate(LoginRequiredMixin, View):

    def post(self, request):    
        book_id = request.POST.get('book_id')
        user_id = request.POST.get('user_id')

        student = Student.objects.get(user=self.request.user)

        user_has_rented_book_already = Order.objects.filter(
            Q(id=book_id) & Q(student=student)
        ).exists()

        number_of_this_book_available = Book.objects.get(id=book_id).quantity

        if number_of_this_book_available > 0 and not user_has_rented_book_already:

            new_order = Order(
                book = Book.objects.get(id=book_id),
                student = User.objects.get(id=user_id).student
            )
            new_order.save()

        # redirect back to page that made initial request
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class StudentLibrary(Library):
    template_name = 'library/student_library.html'    
    permission_required = 'library.is_student'


class LoginRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        if self.request.user.is_staff:
            return redirect(reverse_lazy('admin-library'))
        else:
            return redirect(reverse_lazy('student-collections'))


class SignupView(View):

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
            
            # new user has been added. get and add a student profile to it
            newest_user = User.objects.last()


            # add the new user to a permission group
            student_group = Group.objects.get(name='Student')
            newest_user.groups.add(student_group)
            newest_user.save()

            # Create a student instance and assign new user to it
            new_student = Student(name=newest_user.username, user=newest_user)
            new_student.save()
        
            return redirect('login')
        
        return redirect('.')