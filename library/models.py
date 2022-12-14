from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.auth.models import AbstractUser

# for implementing object permission rules
from rules.contrib.models import RulesModel
from . import permissions


BOOK_HOLDING_TIME = timedelta(days=14)


# Create your models here.

class User(AbstractUser):
    pass


class Book(RulesModel):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    cost = models.IntegerField()
    quantity = models.IntegerField()
    content = models.TextField(null=True, blank=True)

    # object-level permissions
    class Meta:
        rules_permissions = {
            'add': permissions.rules.is_staff,
            'read': permissions.is_staff_or_with_book
        }

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        # fill content with random data
        self.content = f"Chapter 1 of {self.title}: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
        super().save(*args, **kwargs)


class Student(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=500)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Order(RulesModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # object-level permissions
    class Meta:
        rules_permissions = {
            'change': permissions.is_order_creator,  # create perm: "<app>.change_order" from predicate
            'delete': permissions.is_order_creator
        }

    def __str__(self):
        return f"Order: {self.book.title}. Author: {self.book.author}. \
            Ordered by {self.student.name}.\n \
            Issue Date: {self.issue_date} \n  \
            Expiry Date: {self.expiry_date}"


    # overwrite the default save() method
    def save(self, *args, **kwargs) -> None:
        
        if not self.id: # if object does not exist in database yet
            assert self.book.quantity > 0
            
            self.expiry_date = self.issue_date + BOOK_HOLDING_TIME

            # update quantity of this book available for rent
            self.book.quantity -= 1
            self.book.save()

            # subtract from student's available purchasing credits
            self.student.credits -= self.book.cost
            self.student.save()

        return super().save(*args, **kwargs)


    # overwrite the default delete() method
    def delete(self, *args, **kwargs):
        # update quantity of this book available for rent
        self.book.quantity += 1
        self.book.save()

        return super().delete(*args, **kwargs)
