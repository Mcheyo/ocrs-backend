# OCRS Backend - Quick Start Guide

## ⚡ Get Started in 5 Minutes

### Step 1: Prerequisites Check
Ensure you have installed:
- Python 3.11 or higher
- MySQL 8.0 or higher
- Git

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-org/ocrs-backend.git
cd ocrs-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and update these key settings:
# DB_PASSWORD=your_mysql_password
# JWT_SECRET_KEY=generate_a_random_secret_key
# SECRET_KEY=generate_another_random_secret_key
```

### Step 4: Setup Database

```bash
# Run the setup script
python scripts/setup_database.py

# Follow the prompts:
# - Confirm database creation
# - Choose to load sample data (recommended for testing)
```

### Step 5: Run the Application

```bash
# Start the Flask development server
python src/app.py

# The server will start on http://localhost:5000
```

### Step 6: Explore the API

Open your browser and navigate to:
- **API Documentation**: http://localhost:5000/api/docs
- **Health Check**: http://localhost:5000/health

## 🧪 Testing the API

### Using curl

```bash
# Test health endpoint
curl http://localhost:5000/health

# Login (if you loaded seed data)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@umgc.edu","password":"Password123!"}'
```

### Using Swagger UI

1. Go to http://localhost:5000/api/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

## 📝 Test Accounts (After Seeding)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@umgc.edu | Password123! |
| Student | maurice.a@student.umgc.edu | Password123! |
| Faculty | j.smith@umgc.edu | Password123! |

## 🐛 Troubleshooting

### "Cannot connect to MySQL"
- Check if MySQL is running: `mysql -u root -p`
- Verify credentials in `.env` file
- Ensure database user has proper permissions

### "Module not found"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### "Port 5000 already in use"
- Change the port in `.env`: `PORT=5001`
- Or stop the process using port 5000

## 🚀 Next Steps

1. **Review the API docs** at /api/docs
2. **Check the main README.md** for detailed documentation
3. **Run tests**: `pytest`
4. **Start developing**: Create feature branches for your work

## 📞 Need Help?

- Check the main README.md for detailed documentation
- Review the code comments and docstrings
- Ask the team on WhatsApp or Teams
- Create an issue in the GitHub repository

---

**Happy Coding! 🎉**