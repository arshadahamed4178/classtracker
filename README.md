# 📚 ClassTracker – Student & Tutor Management System

ClassTracker is a Django-based web application for managing student and tutor information with workflows for registration, record management, tutor assignment, and search. It uses a MySQL database configured through XAMPP and demonstrates full-stack development with dynamic templates and relational data handling.

# > Note: Requires XAMPP (Apache & MySQL) for database setup.

## 🛠️ Tech Stack
Django 4.2, Python, MySQL (XAMPP), HTML, CSS, Django Templates, Pillow

## ✨ Features
- Student & tutor registration  
- View and manage records  
- Tutor assignment workflow  
- Search and filter functionality  
- Organized academic data management  

## ⚙️ Setup & Run

```bash
# Start Apache & MySQL from XAMPP
# Click on admin in MySql to open the database page

git clone https://github.com/yourusername/classtracker.git
cd classtracker

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Create a database in http://localhost/phpmyadmin
# Example DB name: classtracker_db
# Then update settings.py with your MySQL credentials

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ct_db', # same name to be used to create database
        'USER': 'root',
        'PASSWORD': '', # optional
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

python manage.py migrate
python manage.py runserver
