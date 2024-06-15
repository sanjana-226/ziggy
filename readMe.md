# Ziggy Order Fulfilment Platform

## Overview

Ziggy is a startup that offers on-demand delivery of food and groceries. This project is an operations platform to manage the assignment of delivery executives to on-demand orders. The system includes a backend for handling data storage and processing, and a frontend for user interaction.

## Deployment

### Frontend Deployment

<https://ziggy-nine.vercel.app/>

### Backend Deployment

## Local Setup and Installation

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/delivery-management-system.git
    cd delivery-management-system
    ```

2. Install backend dependencies:

    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3. Install frontend dependencies:

    ```bash
    cd ../frontend
    npm install
    ```

## Backend

### Populating the Database

1. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2. Run the `db.py` file to populate the database:

    ```bash
    python db.py
    ```

    This will populate the database with sample data from `Orders.JSON` and `Drivers.JSON`.

### Running the Backend

1. Start the backend server:

    ```bash
    python app.py
    ```

    The backend server will be available at `http://localhost:5000`.

## Frontend

### Running the Frontend

1. Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2. Start the frontend application:

    ```bash
    ng serve
    ```

    The frontend application will be available at `http://localhost:4200`.
