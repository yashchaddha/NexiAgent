#!/bin/bash

# Startup script for ISO 27001:2022 Auditor Agent with User Memory System
echo "🚀 Starting ISO 27001:2022 Auditor Agent with User Memory System"
echo "================================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please create one first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if database is set up
echo "📊 Checking database setup..."
cd backend
python setup_user_memory.py
if [ $? -ne 0 ]; then
    echo "❌ Database setup failed. Please check your configuration."
    exit 1
fi
cd ..

echo ""
echo "✅ Database is ready!"
echo ""
echo "🚀 To start the system, open 3 terminal windows and run:"
echo ""
echo "Terminal 1 (Authentication Service):"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python login.py"
echo ""
echo "Terminal 2 (Main Agent Service):"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 3 (Frontend):"
echo "  cd frontend"
echo "  source ../venv/bin/activate"
echo "  streamlit run app_with_auth.py"
echo ""
echo "🌐 The system will be available at:"
echo "  - Frontend: http://localhost:8501"
echo "  - Auth API: http://localhost:8001"
echo "  - Main API: http://localhost:8000"
echo ""
echo "🧪 To test the system:"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python test_user_memory.py"
echo ""
echo "📚 For more information, see USER_MEMORY_README.md"
