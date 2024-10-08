# MintyPlay by CogniticCore - Backend Overview 🛠️🎮

## Project Overview 🚀

MintyPlay is a decentralized gaming platform that enables players to earn and own in-game assets as NFTs using blockchain technology. The backend is designed to handle the API services, database management, and blockchain interactions necessary to support the platform’s core features.

This repository contains the backend codebase responsible for the core business logic, database connections, API endpoints, and blockchain integration.

## Key Features ✨

1. **User Management**: Register, login, and manage users 🧑‍💻.
2. **Game Management**: Upload and manage games, monitor gameplay statistics, and player engagement 🎮📊.
3. **NFT Minting**: Mint NFTs for in-game achievements using the TRON blockchain 🏅🔗.
4. **Purchases & Transactions**: Handle transactions using TRX cryptocurrency 💸.
5. **Developer Dashboard**: Manage and track the performance of published games 🛠️.
6. **API Documentation**: Automatically generated API documentation via FastAPI’s `docs` and `redoc` 📄.

## Technology Stack ⚙️

- **Framework**: FastAPI (Python) 🐍⚡
- **Database**: MongoDB 🗄️
- **Blockchain**: TRON for minting NFTs and handling TRX-based transactions 🔗.
- **Containerization**: Docker 🐳
- **API Documentation**: Swagger/OpenAPI via FastAPI 📜

## Backend Architecture 🏗️

The backend is structured using the following components to ensure scalability, modularity, and easy maintainability:

### 1. **API Layer** (`/app/api/v1`) 🌐
   - This layer contains all the API routes grouped by feature, such as users, games, purchases, etc. Each feature is separated into its own file under `/endpoints`.

### 2. **Core Logic** (`/app/core`) 🔧
   - This contains fundamental logic like the connection to the database and interaction with the TRON blockchain (`tron.py`). This layer ensures blockchain-related operations like minting and transactions are handled.

### 3. **Models** (`/app/models`) 🗃️
   - Data models that map to the database schema. For instance, `user_model.py`, `bounty_model.py`, and `nft_model.py` represent the structure of the corresponding data entities.

### 4. **Services** (`/app/services`) 🛠️
   - Contains the business logic for various entities like users, NFTs, purchases, and games. These services interact with the database, perform CRUD operations, and interact with blockchain utilities.

### 5. **Schemas** (`/app/schemas`) 📝
   - Pydantic models used for data validation. These schemas ensure that data exchanged between the API and the frontend is validated and formatted correctly.

### 6. **Exception Handling** (`/app/exceptions`) ❗
   - Custom exception handling, which ensures consistent error reporting across the entire API.

### 7. **Utilities** (`/app/utils`) 🧰
   - Helper functions and utilities to support the main application, such as user helpers and other reusable logic.

## Running the Application 🏃‍♂️

### Prerequisites ✅

- **Docker**: Ensure Docker is installed 🐳.
- **TRON Wallet**: A TRON wallet and TRX tokens are required for NFT-related operations 🔗.
- **Python**: Required if running without Docker 🐍.

run docker
```
docker compose up
```

now you should check your localhost
```
localhost:8000
127.0.0.1:8000
```
read documentation
```
localhost:8000/docs
127.0.0.1:8000/redoc
```

!!! IMPORTANT: Remember to close docker after using !!!

close docker
```
docker compose down
```

check log docker
```
docker compose log
```





## Here is the directory structure with an explaination.


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
    │   __init__.py              # Initializes the app package
    │
    ├── /api                     # Contains all API routes
    │   └── /v1                  # API version 1
    │       │   v1.py            # Main logic for API version 1
    │       │   __init__.py      # Initializes the v1 package
    │       │
    │       └── /endpoints       # API endpoints grouped by feature
    │               ├── bounties.py  # API endpoints related to bounties (listing, creation, etc.)
    │               ├── developers.py # API endpoints related to developers (management, details)
    │               ├── games.py     # API endpoints related to games (listing, creation, etc.)
    │               ├── nfts.py      # API endpoints related to NFTs (listing, details, creation)
    │               ├── orderitem.py  # API endpoints for order items (management, details)
    │               ├── purchases.py   # API endpoints for managing purchases (creation, history)
    │               ├── users.py     # API endpoints related to user management (registration, login)
    │               └── __init__.py  # Initializes the endpoints package
    │
    ├── /core                    # Core application logic and utilities
    │       ├── database.py      # Database connection and management logic
    │       ├── tron.py          # Tron blockchain-related utilities (if applicable)
    │       └── __init__.py      # Initializes the core package
    │
    ├── /exceptions              # Custom exceptions for the application
    │       └── exception_handlers.py # Handles exceptions and errors in the application
    │
    ├── /models                  # Data models for the application
    │       ├── bounty_model.py  # Model for bounty data (fields and validation)
    │       ├── game_model.py    # Model for game data (fields and validation)
    │       ├── nft_model.py     # Model for NFT data (fields and validation)
    │       ├── user_model.py    # Model for user data (fields and validation)
    │       └── __init__.py      # Initializes the models package
    │
    ├── /schemas                 # Pydantic schemas for data validation
    │       ├── bounty_schema.py  # Schema for bounty data validation and serialization
    │       ├── game_schema.py    # Schema for game data validation and serialization
    │       ├── http_exception_schema.py # Schema for handling HTTP exceptions
    │       ├── nft_schema.py     # Schema for NFT data validation and serialization
    │       ├── orderitem_schema.py # Schema for order item data validation
    │       ├── order_schema.py    # Schema for order data validation
    │       ├── purchase_schema.py  # Schema for purchase data validation and serialization
    │       ├── response_schema.py   # Schema for API response validation
    │       ├── user_schema.py      # Schema for user data validation
    │       └── verifiedpurchase_schema.py # Schema for validated purchase data
    │       └── __init__.py         # Initializes the schemas package
    │
    ├── /services                 # Business logic and service layer
    │       ├── bounty_service.py      # Service functions for bounty-related operations
    │       ├── game_service.py        # Service functions for game-related operations
    │       ├── nft_service.py         # Service functions for NFT-related operations
    │       ├── orderitem_service.py   # Service functions for order item-related operations
    │       ├── purchase_service.py    # Service functions for purchase-related operations
    │       ├── user_service.py        # Service functions for user-related operations
    │       ├── verifypurchase_service.py # Service functions for purchase verification
    │       └── __init__.py            # Initializes the services package
    │
    └── /utils                     # Utility functions for the application
        └── /helper                # Helper functions organized in a separate directory
                └── user_helper.py  # Helper functions for user-related operations
```