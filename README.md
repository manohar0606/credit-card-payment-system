# Credit Card Payment System

This is a backend project for managing credit cards and payments.

The project is developed using Django, FastAPI and MySQL.

## Technologies Used

- Python
- Django
- FastAPI
- MySQL
- SQLAlchemy
- JWT
- PyJWT
- Pytest
- Postman

## Features

### User Authentication

- User registration
- User login
- JWT authentication
- Password encryption
- Protected routes
- Logout

### Card Management

- Add credit/debit card
- View saved cards
- Delete card
- Card number masking
- Store last 4 digits
- Card validation
- CVV is not stored

### Payment

- Make payment
- Payment validation
- Payment status
- Card ownership validation
- Transaction creation

### Transaction Management

- View transaction history
- Filter transactions by status
- Filter transactions by amount
- Filter transactions by date
- Export transactions to CSV

### Admin

- Manage users
- Manage cards
- View transactions
- Daily payment summary
- Admin logs

## Database

MySQL is used as the database.

Main tables:

- Users
- Cards
- Transactions
- Admin Logs

## How to Run

First activate the virtual environment:

```bash
myevn\Scripts\activate