from django.contrib import admin
from .models import Book, Borrower, BorrowedBook

admin.site.register(Book)
admin.site.register(Borrower)
admin.site.register(BorrowedBook)
