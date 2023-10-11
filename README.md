# food-delivery-backend

This is a Django-based web application which is createad using django-drf to create API's for various features.

## Prerequisites

- Python 3.x
- pip
- virtualenv (optional, but recommended)

### Install virtualenv if not already installed
  ```
  pip install virtualenv
```
### Create a virtual environment (replace 'venv' with your preferred name)
```
  virtualenv venv
```
### Activate the virtual environment

  #### On Windows:
```
  venv\Scripts\activate
```
  #### On macOS and Linux:
```
  source venv/bin/activate
```
## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/akshay-toshniwal/food-delivery-backend.git
   cd food-delivery-backend
   ```

2. Install Django and project dependencies:

   ```
   pip install -r requirements.txt
   ```
   
3. To start with project
    ```
    cd food-delivery-backend/
    ```

4. Migrate the database:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create superuser (admin):

   ```
   python manage.py createsuperuser
   ```
   Follow the prompts for admin `username`, `password`

6. Run the development server:

   ```
   python manage.py runserver
   ```

7. Access the application in your web browser at http://localhost:8000/
