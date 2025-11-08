# Online Course Registration System (OCRS) - Backend


A comprehensive web-based course registration system built for University of Maryland Global Campus (UMGC) as a capstone project for CMSC-495.

## 📋 Table of Contents

- [🚀 GitHub Setup](#github-setup) ⭐ **Start Here!**
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Team Members](#team-members)

## 🚀 GitHub Setup

**👉 First time setting up? See [GITHUB_QUICK_START.md](GITHUB_QUICK_START.md) for a 3-minute setup guide!**

Quick commands:
```bash
# Linux/Mac - Automated
./scripts/init_git.sh

# Windows - Automated  
scripts\init_git.bat

# Manual (all systems)
git init && git add . && git commit -m "Initial commit" && git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

For detailed instructions and team collaboration setup, see [GITHUB_SETUP.md](GITHUB_SETUP.md).

## 🎯 Overview

The Online Course Registration System (OCRS) is a modern web-based application that simplifies and automates the course enrollment process for students and faculty. The system provides a secure, user-friendly platform for course browsing, enrollment management, and schedule viewing.

### Key Objectives

- Automate student course registration and reduce manual administrative tasks
- Enhance accessibility through a centralized web-based platform
- Improve accuracy and reduce human error in course scheduling
- Deliver a scalable, secure, and maintainable software solution

## ✨ Features

### For Students
- 👤 User account creation and authentication
- 🔍 Course browsing and search by department/time
- 📝 Course enrollment and drop functionality
- 📅 Schedule viewing and management
- ⏰ Waitlist management for full courses
- 📊 Real-time seat availability

### For Faculty
- 📚 Course section management
- 👥 View enrolled students
- 📋 Section scheduling

### For Administrators
- ➕ Add, modify, and remove courses
- 📈 Enrollment statistics and reports
- 👤 User management
- 🔧 System configuration

### System Features
- 🔐 Secure authentication with JWT tokens
- 🔒 Role-based access control (RBAC)
- ✅ Input validation and sanitization
- 📝 Comprehensive audit logging
- 🚦 Rate limiting for API protection
- 📄 API documentation with Swagger

## 🛠️ Technology Stack

- **Backend Framework**: Flask 3.0.0
- **Database**: MySQL 8.0+
- **Authentication**: JWT (Flask-JWT-Extended)
- **Password Hashing**: bcrypt
- **CORS**: Flask-CORS
- **API Documentation**: Flasgger (Swagger UI)
- **Testing**: pytest
- **Logging**: Python JSON Logger

## 📁 Project Structure

```
ocrs-backend/
├── config/
│   ├── __init__.py
│   └── config.py                 # Application configuration
├── database/
│   ├── schema.sql                # Database schema
│   ├── migrations/               # Database migrations
│   └── seeds/
│       └── initial_data.sql      # Seed data
├── docs/
│   └── api/                      # API documentation
├── logs/                         # Application logs
├── src/
│   ├── __init__.py
│   ├── app.py                    # Main application entry point
│   ├── auth/                     # Authentication module
│   ├── courses/                  # Courses module
│   ├── enrollments/              # Enrollments module
│   ├── students/                 # Students module
│   ├── admin/                    # Admin module
│   └── utils/
│       ├── __init__.py
│       ├── database.py           # Database utilities
│       ├── logger.py             # Logging configuration
│       ├── validators.py         # Input validation
│       └── responses.py          # Response formatting
├── tests/
│   ├── unit/                     # Unit tests
│   └── integration/              # Integration tests
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0+**: [Download MySQL](https://dev.mysql.com/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads/)
- **pip**: Python package manager (comes with Python)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ocrs-backend.git
cd ocrs-backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 💾 Database Setup

### 1. Create Database

```bash
# Log into MySQL
mysql -u root -p

# Create database
CREATE DATABASE ocrs_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create database user (optional but recommended)
CREATE USER 'ocrs_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON ocrs_db.* TO 'ocrs_user'@'localhost';
FLUSH PRIVILEGES;

# Exit MySQL
EXIT;
```

### 2. Initialize Schema

```bash
# Run schema creation
mysql -u ocrs_user -p ocrs_db < database/schema.sql
```

### 3. Seed Database (Optional)

```bash
# Load sample data
mysql -u ocrs_user -p ocrs_db < database/seeds/initial_data.sql
```

**Default Test Credentials** (after seeding):
- **Admin**: admin@umgc.edu / Password123!
- **Student**: maurice.a@student.umgc.edu / Password123!
- **Faculty**: j.smith@umgc.edu / Password123!

## ⚙️ Configuration

### 1. Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

### 2. Update .env File

Edit the `.env` file with your settings:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ocrs_db
DB_USER=ocrs_user
DB_PASSWORD=your_secure_password

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_change_this

# Flask
SECRET_KEY=your_flask_secret_key_change_this
FLASK_ENV=development
```

**⚠️ Important**: Never commit the `.env` file to version control!

## 🏃 Running the Application

### Development Mode

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the application
python src/app.py
```

The application will start on `http://localhost:5000`

### Production Mode

For production deployment, use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:5000/api/docs

The API documentation includes:
- All available endpoints
- Request/response formats
- Authentication requirements
- Example requests

## 🧪 Testing

### Run All Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_auth.py
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database operations

## 👥 Team Members

**CMSC-495 Group 3 - Fall 2025**

- Christopher Davis (Project Lead)
- Maurice Adovoekpe
- Mansour Cheyo
- Nelvis Lumvalla
- Sritej Nadella
- Steven Nguyen
- Michael Sibley Jr.
- Xu Wang
- Ronell Wilder

## 📄 License

This project is developed as a capstone project for University of Maryland Global Campus.

## 🤝 Contributing

This is an academic capstone project. For team members:

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m 'Add some feature'`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Submit a pull request

### Coding Standards

- Follow PEP 8 style guide for Python code
- Write docstrings for all functions and classes
- Add unit tests for new features
- Update API documentation as needed

## 📞 Support

For questions or issues:
- Create an issue in the GitHub repository
- Contact the team lead: chris.davis@umgc.edu

## 🔄 Version History

- **v1.0.0** (November 2025) - Initial release with core functionality

---

**University of Maryland Global Campus**  
CMSC-495 Computer Science Capstone  
Fall 2025