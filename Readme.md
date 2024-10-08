# MintyPlay by CogniticCore 🎮🚀

**MintyPlay** is a decentralized gaming platform enabling players to earn and own in-game assets as NFTs through blockchain technology. This repository contains both **Frontend** and **Backend** codebases, designed for a seamless and immersive gaming experience.

---

## Table of Contents

1. [Frontend Overview](#frontend-overview)
   - [Getting Started](#getting-started)
   - [Key Features](#key-features)
   - [Technology Stack](#technology-stack)
   - [Running the Application](#running-the-application)
   - [Directory Structure](#frontend-directory-structure)

2. [Backend Overview](#backend-overview)
   - [Key Features](#backend-key-features)
   - [Technology Stack](#backend-technology-stack)
   - [Architecture](#backend-architecture)
   - [Running the Application](#running-the-backend-application)
   - [Directory Structure](#backend-directory-structure)

---

## Frontend Overview 🌐

The **MintyPlay** frontend offers an intuitive interface, enhancing user interaction with the platform.

### Getting Started

Ensure you have Node.js and npm/yarn installed. Follow these steps:

1. Clone the repository.
2. Install dependencies:

   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:

   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Access the application at [http://localhost:3000](http://localhost:3000).

### Key Features

- **User Authentication**: Secure login and registration.
- **Responsive UI**: Adapts to various screen sizes.
- **NFT Marketplace**: Buy, sell, and view NFTs.
- **Game Dashboard**: Monitor gameplay statistics and achievements.

### Technology Stack

- **Framework**: Next.js
- **Styling**: CSS Modules, Tailwind CSS
- **State Management**: Redux Toolkit
- **API Integration**: Axios
- **Deployment**: Vercel

### Frontend Directory Structure

```
frontend
│
├── public                        # Static files
├── src
│   ├── components                # Reusable components
│   ├── pages                     # Application pages
│   ├── store                     # Redux store
│   ├── styles                    # Global styles
│   └── utils                     # Utility functions
└── package.json                  # Project metadata and dependencies
```

---

## Backend Overview 🛠️

The **MintyPlay** backend manages API services, database operations, and blockchain interactions, providing a robust foundation.

### Backend Key Features

- **User Management**: Tools for user registration and management.
- **Game Management**: Upload and monitor games.
- **NFT Minting**: Create NFTs on the TRON blockchain.
- **Developer Dashboard**: Analyze game performance.
- **API Documentation**: Auto-generated via FastAPI.

### Backend Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Blockchain**: TRON for NFT minting
- **Containerization**: Docker
- **API Documentation**: Swagger/OpenAPI via FastAPI

### Backend Architecture

The backend is designed for scalability and maintainability, featuring:

- **API Layer**: Organized routes by feature.
- **Core Logic**: Database and blockchain operations.
- **Models**: Database schema representations.
- **Services**: Business logic for users and NFTs.
- **Schemas**: Data validation with Pydantic.
- **Utilities**: Helper functions for application functionality.

### Prerequisites ✅

- **Docker**: Install Docker.
- **TRON Wallet**: Required for NFT operations.
- **Python**: Necessary if running without Docker.

### Running the Backend Application

1. Ensure Docker is installed.
2. Start the Docker containers:

   ```bash
   docker compose up
   ```

3. Access the application at:

   - Main Application: [http://localhost:8000](http://localhost:8000)
   - Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

4. To stop Docker:

   ```bash
   docker compose down
   ```


### Backend Directory Structure


```
backend
│
├── .env                         # Environment variables for configuration
├── .gitignore                   # Specifies files to ignore in version control
├── docker-compose.yml           # Docker Compose file for defining and running multi-container Docker applications
├── Dockerfile                   # Instructions for building the Docker image
├── README.md                    # Documentation for the project
├── requirements.txt             # List of dependencies required for the project
│
└── /app                         # Main application directory
    │   main.py                  # Entry point of the application
    │
    ├── /api                     # Contains all API routes
    │   └── /v1                  # API version 1
    │       │   v1.py            # Main logic for API version 1
    │       │
    │       └── /endpoints       # API endpoints grouped by feature
    │
    ├── /core                    # Core application logic and utilities
    │
    ├── /exceptions              # Custom exceptions for the application
    │
    ├── /models                  # Data models for the application
    │
    ├── /schemas                 # Pydantic schemas for data validation
    │
    ├── /services                 # Business logic and service layer
    │
    └── /utils                     # Utility functions for the application
        └── /helper                # Helper functions organized in a separate directory
```
