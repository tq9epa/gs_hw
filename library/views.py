from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Borrower, BorrowedBook
from .serializers import BookSerializer, BorrowerSerializer, BorrowedBookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        try:
            book = self.get_object()
            if book.is_borrowed:
                return Response({"error": "Book is already borrowed."}, status=status.HTTP_400_BAD_REQUEST)

            borrower_id = request.data.get('borrower_id')
            borrower = Borrower.objects.get(pk=borrower_id)

            BorrowedBook.objects.create(book=book, borrower=borrower)
            book.is_borrowed = True
            book.save()

            return Response({"message": "Book borrowed successfully."}, status=status.HTTP_200_OK)
        except Borrower.DoesNotExist:
            return Response({"error": "Borrower not found."}, status=status.HTTP_404_NOT_FOUND)


class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

    @action(detail=True, methods=['get'])
    def borrowed_books(self, request, pk=None):
        try:
            borrower = self.get_object()
            borrowed_books = BorrowedBook.objects.filter(borrower=borrower)
            serializer = BorrowedBookSerializer(borrowed_books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Borrower.DoesNotExist:
            return Response({"error": "Borrower not found."}, status=status.HTTP_404_NOT_FOUND)
