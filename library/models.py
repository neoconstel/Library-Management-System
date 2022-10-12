from email.policy import default
from statistics import mode
from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta

BOOK_HOLDING_TIME = timedelta(days=14)


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    cost = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"


class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.book.title}. Author: {self.book.author}. \
            Ordered by {self.student.name}.\n \
            Issue Date: {self.issue_date} \n  \
            Expiry Date: {self.expiry_date}"


    # overwrite the default save() method
    def save(self, *args, **kwargs) -> None:
        if not self.id: # if object does not exist in database yet
            self.expiry_date = self.issue_date + BOOK_HOLDING_TIME

        return super().save(*args, **kwargs)