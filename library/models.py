from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_borrowed = models.BooleanField(default=False)

class Borrower(models.Model):
    name = models.CharField(max_length=255)

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
