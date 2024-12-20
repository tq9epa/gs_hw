# Library Management System (Django + PostgreSQL)

This document provides step-by-step instructions to set up and run the Library Management System on a Windows OS.

---

## **1. Prerequisites**

Before starting, ensure you have the following installed:

- **Python 3.10 or later**: Download from [python.org](https://www.python.org/downloads/).
- **PostgreSQL**: Download and install from [postgresql.org](https://www.postgresql.org/download/).
- **pip**: Python's package manager (usually installed with Python).
- **Git**: Optional but useful for cloning the repository.

---

## **2. Clone the Repository**

If you are using Git, clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

Alternatively, download the repository as a ZIP file and extract it.

---

## **3. Set Up the Virtual Environment**

1. Open Command Prompt (or PowerShell).
2. Navigate to the project directory:
   ```bash
   cd <repository_directory>
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

   You should see `(env)` at the beginning of the command line.

---

## **4. Install Dependencies**

Run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn’t exist, install these packages manually:

```bash
pip install django djangorestframework psycopg2-binary
```

---

## **5. Configure PostgreSQL**

1. Open the PostgreSQL installation directory and launch **SQL Shell (psql)**.
2. Log in with your PostgreSQL username and password.
3. Create a new database:
   ```sql
   CREATE DATABASE library_db;
   ```
4. Create a new PostgreSQL user (optional):
   ```sql
   CREATE USER library_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
   ```

---

## **6. Configure Django Settings**

1. Open `library_management/settings.py`.
2. Update the `DATABASES` setting:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'library_db',
           'USER': 'library_user',
           'PASSWORD': 'your_password',
           'HOST': '127.0.0.1',
           'PORT': '5432',
       }
   }
   ```

---

## **7. Apply Migrations**

Run the following commands to initialize the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **8. Create a Superuser**

To access the Django Admin interface, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up a username, email, and password.

---

## **9. Run the Development Server**

Start the server by running:

```bash
python manage.py runserver
```

Access the application at:

- API Endpoints: `http://127.0.0.1:8000/api/`
- Admin Interface: `http://127.0.0.1:8000/admin/`

---

## **10. Testing the Application**

Run the test suite to ensure everything works as expected:

```bash
python manage.py test
```

---

## **11. Interacting with the API**

### Endpoints:

- **Books**:
  - List: `GET /api/books/`
  - Add: `POST /api/books/`
  - Borrow: `POST /api/books/<id>/borrow/`
- **Borrowers**:
  - List: `GET /api/borrowers/`
  - Add: `POST /api/borrowers/`
  - Borrowed Books: `GET /api/borrowers/<id>/borrowed_books/`

Use tools like **Postman** or the Django Browsable API to interact with these endpoints.

---

## **12. Common Issues and Fixes**

### **Issue: PostgreSQL connection error**
- Ensure PostgreSQL is running.
- Double-check your `DATABASES` configuration in `settings.py`.

### **Issue: `relation "library_book" does not exist`**
- Ensure migrations are applied: `python manage.py migrate`.

### **Issue: Environment variables not set**
- Ensure the virtual environment is activated: `.\env\Scripts\activate`.

---

Congratulations! Your Library Management System should now be running on Windows!

