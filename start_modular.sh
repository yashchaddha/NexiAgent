#!/bin/bash

# Startup script for ISO 27001:2022 Auditor Agent with Modular Architecture
echo "🚀 Starting ISO 27001:2022 Auditor Agent with Modular Architecture"
echo "=================================================================="

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
echo "🏗️  **New Modular Architecture Detected!**"
echo "   The backend has been refactored into clean, focused modules:"
echo "   - main.py: Application entry point (~50 lines)"
echo "   - agent_graph.py: Agent workflow logic"
echo "   - api_routes.py: API endpoint handlers"
echo "   - knowledge_base.py: ISO 27001:2022 knowledge"
echo "   - dependencies.py: Shared utilities"
echo "   - conversation_service.py: User memory management"
echo ""
echo "🚀 To start the system, open 3 terminal windows and run:"
echo ""
echo "Terminal 1 (Authentication Service):"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python login.py"
echo ""
echo "Terminal 2 (Main Agent Service - NEW MODULAR):"
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
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "🧪 To test the new modular system:"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python test_memory_simple.py"
echo ""
echo "🎭 To run the full demo:"
echo "  cd backend"
echo "  source ../venv/bin/activate"
echo "  python demo_user_memory.py"
echo ""
echo "📚 Documentation:"
echo "  - MODULAR_ARCHITECTURE_README.md - New architecture details"
echo "  - USER_MEMORY_README.md - User memory system features"
echo ""
echo "🔍 **API Changes in New Architecture:**"
echo "  - All API routes now prefixed with /api/v1"
echo "  - Example: /query is now /api/v1/query"
echo "  - Root endpoints remain at / and /health"
echo "  - Full API documentation available at /docs"
echo ""
echo "✨ **Benefits of New Architecture:**"
echo "  ✅ Cleaner, more maintainable code"
echo "  ✅ Easier to add new features"
echo "  ✅ Better separation of concerns"
echo "  ✅ Improved testing capabilities"
echo "  ✅ Professional code organization"
echo ""
echo "🎉 **Ready to Launch!**"
echo "   The new modular architecture is fully functional and ready to use!"
