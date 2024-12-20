from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Borrower, BorrowedBook

class LibraryIntegrationTests(TestCase):
    def setUp(self):
        # Initialize test client
        self.client = APIClient()

        # Test data
        self.borrower_payload = {"name": "John Doe"}
        self.book_payload = {"title": "Django for APIs", "author": "William S. Vincent"}

    def test_end_to_end_workflow(self):
        """
        Test an end-to-end workflow:
        1. Create a borrower.
        2. Create a book.
        3. Borrow the book.
        4. List borrowed books by the borrower.
        """
        # Step 1: Create a borrower
        borrower_response = self.client.post('/api/borrowers/', self.borrower_payload)
        self.assertEqual(borrower_response.status_code, status.HTTP_201_CREATED)
        borrower_id = borrower_response.data['id']

        # Step 2: Create a book
        book_response = self.client.post('/api/books/', self.book_payload)
        self.assertEqual(book_response.status_code, status.HTTP_201_CREATED)
        book_id = book_response.data['id']

        # Step 3: Borrow the book
        borrow_payload = {"borrower_id": borrower_id}
        borrow_response = self.client.post(f'/api/books/{book_id}/borrow/', borrow_payload)
        self.assertEqual(borrow_response.status_code, status.HTTP_200_OK)

        # Step 4: List borrowed books by the borrower
        borrowed_books_response = self.client.get(f'/api/borrowers/{borrower_id}/borrowed_books/')
        self.assertEqual(borrowed_books_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(borrowed_books_response.data), 1)
        self.assertEqual(borrowed_books_response.data[0]['book'], book_id)

    def test_borrow_multiple_books(self):
        """
        Test borrowing multiple books by the same borrower.
        """
        # Create borrower
        borrower_response = self.client.post('/api/borrowers/', self.borrower_payload)
        self.assertEqual(borrower_response.status_code, status.HTTP_201_CREATED)
        borrower_id = borrower_response.data['id']

        # Create multiple books
        book1_response = self.client.post('/api/books/', {"title": "Book 1", "author": "Author 1"})
        book2_response = self.client.post('/api/books/', {"title": "Book 2", "author": "Author 2"})
        self.assertEqual(book1_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book2_response.status_code, status.HTTP_201_CREATED)
        book1_id = book1_response.data['id']
        book2_id = book2_response.data['id']

        # Borrow both books
        self.client.post(f'/api/books/{book1_id}/borrow/', {"borrower_id": borrower_id})
        self.client.post(f'/api/books/{book2_id}/borrow/', {"borrower_id": borrower_id})

        # Verify both books are borrowed by the borrower
        borrowed_books_response = self.client.get(f'/api/borrowers/{borrower_id}/borrowed_books/')
        self.assertEqual(borrowed_books_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(borrowed_books_response.data), 2)

    def test_borrow_and_return_flow(self):
        """
        Test borrowing and returning a book.
        """
        # Create borrower and book
        borrower_response = self.client.post('/api/borrowers/', self.borrower_payload)
        borrower_id = borrower_response.data['id']
        book_response = self.client.post('/api/books/', self.book_payload)
        book_id = book_response.data['id']

        # Borrow the book
        borrow_payload = {"borrower_id": borrower_id}
        borrow_response = self.client.post(f'/api/books/{book_id}/borrow/', borrow_payload)
        self.assertEqual(borrow_response.status_code, status.HTTP_200_OK)

        # Verify the book's status is updated
        book_status_response = self.client.get(f'/api/books/{book_id}/')
        self.assertEqual(book_status_response.status_code, status.HTTP_200_OK)
        self.assertTrue(book_status_response.data['is_borrowed'])
