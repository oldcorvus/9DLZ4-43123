
# Restaurant Booking System

A RESTful API for managing restaurant table reservations. This system allows authenticated users to book and cancel reservations while ensuring optimal table allocation and pricing.

## Features

- **Pricing Strategy**: Calculate costs based on individual seats or full table bookings.
- **Concurrency Control**: Handle high traffic with Redis-based locking and database-level locking.
- **OpenAPI Specification**: Fully documented API endpoints using OpenAPI.

## Technologies Used

- **Python**: 3.x
- **Django**: Web framework for building the API.
- **Django REST Framework**: For building RESTful APIs.
- **PostgreSQL**: Database for storing reservations and tables.
- **Redis**: For high-concurrency locking.
- **Docker**: For containerization and deployment.
- **OpenAPI**: For API documentation.
- **Pydantic**: For validating objects.

## Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.x
- PostgreSQL
- Redis

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/oldcorvus/9DLZ4-43123.git
   cd 9DLZ4-43123
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```plaintext
    DEBUG=True
    POSTGRES_USER=test
    POSTGRES_PASSWORD=password
    POSTGRES_DB=test_db
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432

   ```

3. **Build and Run with Docker**:
   ```bash
   docker-compose up --build
   ```

4. **Run Migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Access the API**:
   The API will be available at `http://localhost:8000`.

## API Documentation

The API is documented using OpenAPI. You can access the Swagger UI at:
```
http://localhost:8000/api/docs/
```


### Endpoints

#### 1. **Book a Table**
- **Method**: `POST`
- **URL**: `bookings/`
- **Request Body**:
  ```json
  {
    "num_individuals": 4
  }
  ```
- **Response**:
  ```json
  
    {
        "id": "6367d968-7376-4a58-b6b7-f7fa2c889173",
        "user": 1,
        "table": "690399a1-1b60-4e8c-96c0-83d40bdb951d",
        "start_time": null,
        "end_time": null,
        "cost_amount": "70.00",
        "cost_currency": "USD",
        "status": "CFM",
        "created_at": "2025-02-14T23:42:10.159788Z",
        "updated_at": "2025-02-14T23:42:10.159825Z"
    }
  ```

#### 2. **Cancel a Reservation**
- **Method**: `DELETE`
- **URL**: `/reservations/cance/{reservation_id}/`
- **Response**:
  ```json
  {
    "message": "Reservation cancelled successfully"
  }
  ```

## Business Logic

### Pricing Strategy
- **Individual Seats**: Cost is calculated as `num_individuals * seat_price`.
- **Full Table**: Cost is calculated as `(table_seats - 1) * seat_price`.


### Concurrency Control
- **Normal Load**: Uses database-level locking (`select_for_update`).
- **High Load**: Uses Redis-based locking to handle high traffic.

