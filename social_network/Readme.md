# Social Networking API

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Dockerization](#dockerization)

## Introduction

This is a Django Rest Framework (DRF) API for a social networking application. It allows users to perform various actions like user authentication, sending/receiving friend requests, listing friends, and more.

## Installation

1. Clone the repository:
`bash
git clone <repository_url>
cd social_network
`
2. Create a virtual environment (optional but recommended):

`bash
python -m venv venv
source venv/bin/activate  # On Windows, use "venv\Scripts\activate"
`
3. Install project dependencies:

`bash
pip install -r requirements.txt
`

4. Set up the database:

5. Configure your MySQL database settings in settings.py.
6. Run migrations to create database tables:

7. bash
`
python manage.py makemigrations
python manage.py migrate
`
Set up environment variables (if needed):

You can use environment variables for sensitive information like secret keys and database credentials.
Start the development server:

`bash
python manage.py runserver
`

## Usage
- Register a new user using the signup API endpoint.
- Obtain an access token by sending a POST request to the token obtain endpoint with your email and password.
- Use the access token for authentication when making requests to protected endpoints.
- Explore the various API endpoints for social networking features.

## API Endpoints
- User Signup: /api/signup/ (POST)
- Token Obtain: /api/token/ (POST)
- Search Users: /api/search-users/ (GET)
- Send Friend Request: /send-friend-request/<receiver_id>/ (POST)
- Accept Friend Request: /accept-friend-request/<receiver_id>/ (POST)
- Reject Friend Request: /reject-friend-request/<receiver_id>/ (POST)
- List Friends: /api/list-friends/ (GET)
- List Pending Requests: /api/list-pending-requests/ (GET)

# Dockerization
The project can be containerized using Docker. Use the provided Dockerfile and docker-compose.yml to set up the application and database containers. Follow these steps:
Install Docker and Docker Compose.
Build the Docker containers:
`bash
docker-compose build
`
Start the containers:
`docker-compose up
`