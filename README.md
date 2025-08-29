Hotel Management System CLI 🏨
A command-line interface (CLI) application for managing a hotel. This system allows you to manage rooms, guests, and bookings efficiently. It is built with Python and uses SQLAlchemy for database management.

Features
Room Management: Add, view, and manage hotel rooms.

Guest Management: Add, view, and manage guest information.

Booking System: Create and manage bookings by linking rooms and guests.

Database Integration: All data is persisted in an SQLite database using SQLAlchemy and Alembic for migrations.

Prerequisites
To run this project, you need to have the following installed on your system:

Python 3.12+

pipenv for dependency management.

Installation & Setup
Follow these steps to get a local copy of the project up and running.

Clone the repository:

git clone https://github.com/your-username/Hotel-Management-System.git
cd Hotel-Management-System

Install dependencies:
This will install all the necessary packages defined in the Pipfile.

pipenv install

Activate the virtual environment:

pipenv shell

Run database migrations:
This step sets up your database tables. Make sure you've correctly configured your alembic.ini file.

pipenv run alembic upgrade head

🚀 Usage
Once the setup is complete, you can run the application and its commands from the root directory of the project.

General Command Syntax:

pipenv run python -m hotel_management [command]

Example Commands:

Add a new room:

pipenv run python -m hotel_management add-room

Add a new guest:

pipenv run python -m hotel_management add-guest

Create a new booking:

pipenv run python -m hotel_management book-room

View all rooms:

pipenv run python -m hotel_management view-rooms

📝 Database & Migrations
The project uses a SQLite database, stored in a file named hotel_management.db. Database migrations are handled by Alembic, ensuring your database schema can be easily updated over time.

