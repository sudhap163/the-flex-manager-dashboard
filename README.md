# The Flex Review Management System

## Overview

This project is a full-stack application for The Flex, a property management company, to efficiently manage and approve public reviews. The system consists of a Python backend that handles API requests and a frontend web dashboard built using HTML and CSS for managers to view, filter, and approve reviews.

## Project Structure

The project is organized into a clear, modular structure:
* `/app`: Contains the core backend logic, including controllers, services, and models.
    * `controllers/`: Handles incoming API requests and manages review data.
    * `core/`: Contains fundamental components like database connection (database.py).
    * `models/`: Defines the data models (review_model.py).
    * `services/`: Business logic for data manipulation (review_service.py).
    * `utils/`: Utility functions for configuration and logging.

* `views/`: Frontend files, including the manager dashboard (dashboard.html) and the property page (index.html).
* `/` (root directory):
    * `.gitignore`: Specifies files to be ignored by Git.
    * `config.yaml`: Configuration file for the backend.
    * `README.md`: This file.
    * `requirements.txt`: Python dependencies for the backend.
    * `reviews.db`: The SQLite database file (created after application starts).

## Features

### Frontend Dashboard (`dashboard.html`)

The dashboard is a single-page web application designed for property managers.

* **Live Data Fetching with Elegant Loading:** Automatically fetches review data from the backend API upon page load. A loading state with a spinner is displayed until the data is ready.

* **Dynamic Metrics Card:** A single, dynamic card displays key metrics, switching between overall performance and per-property statistics based on filter selection.

* **Interactive Filtering:** Filter reviews by listing, channel, overall rating, review type (guest-to-host or host-to-guest), date range, and approval status.

* **Dynamic Sorting:** Sort reviews by overall rating or specific category ratings.

* **Review Approval System:** Easily approve reviews for public display with real-time updates to the backend.

* **Responsive Design:** The layout is fully responsive, providing an optimal viewing experience on all devices.

### Backend API

The Python backend provides the necessary API endpoints to support the dashboard's functionality.

* `GET /api/reviews/hostaway`: Fetches all review data.

* `POST /api/reviews/save`: Saves a review's approval status in the database.

## How to Run
1. **Start the Backend:**
    1. Navigate to the project root and install all dependencies by running `pip install -r requirements.txt`
    2. Run the Python backend using command `python app`. The server needs to be running and accessible at http://127.0.0.1:8000.
2. **Open the Dashboard:**
    1. Open the dashboard.html file in your web browser.
    
The dashboard will automatically connect to the backend, fetch the data, and populate the tables and charts.

## Technologies Used
* **Frontend:** HTML5, JavaScript, Tailwind CSS, Chart.js
* **Backend:** Python, FastAPI, SQLite