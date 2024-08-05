# Project README

## Backend Server Documentation

### Introduction

This project is a backend server built using Node.js, Express, and MongoDB. It supports user authentication, file uploads for processing, and data predictions. The server uses Nodemon for development purposes to automatically restart the server on file changes.

### Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Login](#login)
  - [Register](#register)
  - [Upload Data](#upload-data)
  - [Predictions](#predictions)
- [Database](#database)
- [Error Handling](#error-handling)
- [Dependencies](#dependencies)

### Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone <repository-url>
cd <project-directory>
npm install
```

### Configuration

Create a `.env` file in the root of your project and add the following environment variables:

```plaintext
MONGO_URI=<your-mongodb-uri>
PORT=<your-server-port>
JWT_SECRET=<your-jwt-secret>
```

### Running the Server

To start the server in development mode using Nodemon:

```bash
npm run dev
```

To start the server in production mode:

```bash
npm start
```

### API Endpoints

#### Login

**Endpoint:** `/Login`  
**Method:** `POST`  
**Description:** Authenticates a user and returns a JWT token.  

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "token": "jwt-token",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "username"
  }
}
```

#### Register

**Endpoint:** `/Register`  
**Method:** `POST`  
**Description:** Registers a new user.  

**Request Body:**
```json
{
  "name": "username",
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "username"
  }
}
```

#### Upload Data

**Endpoint:** `/uploadData`  
**Method:** `POST`  
**Description:** Uploads files for processing.  

**Request Body:**
- `file`: The file to be uploaded (multipart/form-data)

**Response:**
```json
{
  "message": "File uploaded successfully",
  "fileId": "file-id"
}
```

#### Predictions

**Endpoint:** `/predictions`  
**Method:** `GET`  
**Description:** Sends processed data in JSON format.  

**Response:**
```json
{
  "predictions": [
    {
      "id": "prediction-id",
      "result": "prediction-result"
    },
    ...
  ]
}
```

### Database

The project uses MongoDB to store user information and uploaded data. Ensure that your MongoDB server is running and the `MONGO_URI` in your `.env` file is correctly configured.

### Error Handling

The server includes basic error handling for common scenarios, such as invalid input, authentication errors, and server errors. Custom error messages are sent in the response to help with debugging and user feedback.

### Dependencies

- **express**: Web framework for Node.js.
- **mongoose**: MongoDB object modeling tool.
- **jsonwebtoken**: For creating and verifying JWT tokens.
- **bcryptjs**: For hashing and comparing passwords.
- **multer**: Middleware for handling `multipart/form-data`.
- **nodemon**: For automatic server restarts during development.

---