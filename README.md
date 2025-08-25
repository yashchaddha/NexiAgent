# 🔐 ISO 27001:2022 Auditor Agent with Authentication

An intelligent agent acting as an expert Internal Auditor of ISO 27001:2022 compliance framework, capable of answering user queries with memory and user authentication.

## 🚀 Features

- **Expert Knowledge**: Comprehensive ISO 27001:2022 compliance guidance
- **Memory System**: Remembers conversation context across sessions
- **User Authentication**: Secure login/signup with JWT tokens
- **PostgreSQL Database**: Persistent user data storage
- **Modern UI**: Beautiful Streamlit interface with dark theme
- **Real-time Chat**: Interactive chat interface with typing animations
- **Session Management**: Multiple concurrent user sessions
- **Auto-scroll**: Automatic scrolling to latest messages
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Main API      │    │   PostgreSQL    │
│   (Streamlit)   │◄──►│   (Port 8000)   │◄──►│   Database      │
│   Port 8501     │    │   + LangGraph   │    │   + Users       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              ▲
                              │
                       ┌─────────────────┐
                       │   Auth API      │
                       │   (Port 8001)   │
                       │   + JWT         │
                       └─────────────────┘
```

## 📁 Project Structure

```
completeAgent/
├── frontend/
│   └── app.py                 # Streamlit UI application
├── backend/
│   ├── main.py                # Main auditor API (LangGraph + FastAPI)
│   ├── login.py               # Authentication API server
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic data validation
│   ├── auth.py                # Authentication utilities
│   ├── init_db.py             # Database initialization
│   ├── test_auth.py           # Authentication tests
│   └── README_AUTH.md         # Authentication documentation
├── requirements.txt            # Python dependencies
├── start.py                   # Start main auditor only
├── start_auth.py              # Start both servers
├── demo.py                    # Demo script with memory
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up PostgreSQL

Make sure PostgreSQL is running:

```bash
# macOS
brew services start postgresql

# Ubuntu/Debian
sudo systemctl start postgresql
```

### 3. Configure Environment

Copy and edit the environment template:

```bash
cd backend
cp env_template.txt .env
```

Edit `.env` with your database credentials:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=iso_auditor_db
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Initialize Database

```bash
cd backend
python init_db.py
```

### 5. Start Both Servers

```bash
# From project root
python start_auth.py
```

This starts:
- **Authentication Server**: Port 8001
- **Main Auditor Server**: Port 8000

### 6. Start Frontend

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

## 🔐 Authentication System

### User Registration Fields

- **Name**: Full name
- **Email**: Unique email address
- **Organization Name**: Company name
- **Domain**: Business domain (Technology, Healthcare, etc.)
- **Location**: Geographic location
- **Organization URL**: Company website (optional)
- **Password**: Secure password

### API Endpoints

| Service | Port | Endpoints |
|---------|------|-----------|
| **Auth API** | 8001 | `/signup`, `/login`, `/profile`, `/health` |
| **Main API** | 8000 | `/query`, `/session/*`, `/health` |

### Security Features

- **JWT Tokens**: Secure, time-limited access
- **Password Hashing**: Bcrypt with salt
- **CORS Protection**: Cross-origin request handling
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🧪 Testing

### Test Authentication

```bash
cd backend
python test_auth.py
```

### Test Main Auditor

```bash
cd backend
python test_backend.py
```

### Manual Testing

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health

# User signup
curl -X POST http://localhost:8001/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","organization_name":"Test Corp","domain":"Technology","location":"Test City","password":"TestPass123!"}'
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `postgres` | Database username |
| `POSTGRES_PASSWORD` | `password` | Database password |
| `POSTGRES_HOST` | `localhost` | Database host |
| `POSTGRES_PORT` | `5432` | Database port |
| `POSTGRES_DB` | `iso_auditor_db` | Database name |
| `SECRET_KEY` | `your-secret-key` | JWT secret key |
| `OPENAI_API_KEY` | - | OpenAI API key |

### Ports

- **Frontend**: 8501 (Streamlit)
- **Main API**: 8000 (FastAPI + LangGraph)
- **Auth API**: 8001 (FastAPI + PostgreSQL)

## 📚 API Documentation

Once servers are running:

- **Main API Docs**: http://localhost:8000/docs
- **Auth API Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8000/redoc, http://localhost:8001/redoc

## 🎯 Usage Examples

### 1. User Registration

```python
import requests

# Sign up
response = requests.post("http://localhost:8001/signup", json={
    "name": "John Doe",
    "email": "john@example.com",
    "organization_name": "TechCorp Inc",
    "domain": "Technology",
    "location": "San Francisco, CA",
    "password": "SecurePass123!"
})
```

### 2. User Login

```python
# Login
response = requests.post("http://localhost:8001/login", json={
    "email": "john@example.com",
    "password": "SecurePass123!"
})

token = response.json()["access_token"]
```

### 3. Ask ISO 27001 Questions

```python
# Ask question with authentication
headers = {"Authorization": f"Bearer {token}"}
response = requests.post("http://localhost:8000/query", json={
    "query": "How do I implement access control policies?",
    "session_id": "user_session_123"
}, headers=headers)
```

## 🚨 Production Considerations

### Security
- Change default `SECRET_KEY`
- Use strong database passwords
- Enable HTTPS
- Restrict CORS origins
- Implement rate limiting

### Database
- Use connection pooling
- Regular backups
- Monitor performance
- Database migrations

### Deployment
- Environment-specific configs
- Health checks
- Monitoring and alerting
- Reverse proxy (nginx)

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   lsof -ti:8000 | xargs kill -9  # Main API
   lsof -ti:8001 | xargs kill -9  # Auth API
   ```

2. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify credentials in `.env`
   - Ensure database exists

3. **Import Errors**
   - Check Python path
   - Verify dependencies installed
   - Check file permissions

### Debug Mode

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 🤝 Contributing

1. Follow existing code structure
2. Add tests for new features
3. Update documentation
4. Use type hints and docstrings
5. Follow PEP 8 style guidelines

## 📄 License

This project is for educational and professional use in ISO 27001:2022 compliance.

---

**Need Help?** Check the authentication README (`backend/README_AUTH.md`) or create an issue in the repository.
