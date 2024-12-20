from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Borrower, BorrowedBook

class LibraryManagementTests(TestCase):
    def setUp(self):
        # Initialize test client
        self.client = APIClient()

        # Create test data
        self.borrower = Borrower.objects.create(name="John Doe")
        self.book1 = Book.objects.create(title="Python Crash Course", author="Eric Matthes", is_borrowed=False)
        self.book2 = Book.objects.create(title="Django for Beginners", author="William S. Vincent", is_borrowed=False)

    def test_list_books(self):
        """Test retrieving a list of all books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_add_book(self):
        """Test adding a new book"""
        payload = {
            "title": "Fluent Python",
            "author": "Luciano Ramalho"
        }
        response = self.client.post('/api/books/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "Fluent Python")

    def test_borrow_book(self):
        """Test borrowing a book"""
        payload = {
            "borrower_id": self.borrower.id
        }
        response = self.client.post(f'/api/books/{self.book1.id}/borrow/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertTrue(self.book1.is_borrowed)

    def test_borrow_book_already_borrowed(self):
        """Test borrowing a book that is already borrowed"""
        self.book1.is_borrowed = True
        self.book1.save()
        payload = {
            "borrower_id": self.borrower.id
        }
        response = self.client.post(f'/api/books/{self.book1.id}/borrow/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_borrow_book_invalid_borrower(self):
        """Test borrowing a book with an invalid borrower ID"""
        payload = {
            "borrower_id": 999  # Nonexistent borrower ID
        }
        response = self.client.post(f'/api/books/{self.book1.id}/borrow/', payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_borrowers(self):
        """Test retrieving a list of all borrowers"""
        response = self.client.get('/api/borrowers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_borrower(self):
        """Test creating a new borrower"""
        payload = {
            "name": "Jane Smith"
        }
        response = self.client.post('/api/borrowers/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrower.objects.count(), 2)
        self.assertEqual(Borrower.objects.last().name, "Jane Smith")

    def test_borrowed_books(self):
        """Test retrieving the list of books borrowed by a borrower"""
        BorrowedBook.objects.create(book=self.book1, borrower=self.borrower)
        response = self.client.get(f'/api/borrowers/{self.borrower.id}/borrowed_books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['book'], self.book1.id)

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
