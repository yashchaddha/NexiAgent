#!/bin/bash

# ISO 27001:2022 Auditor Agent Startup Script

echo "🔒 ISO 27001:2022 Auditor Agent"
echo "====================================="
echo "Built with FastAPI, LangGraph & Streamlit"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ .env file created from template"
        echo "⚠️  Please edit .env and add your OpenAI API key before continuing"
        echo "   You can edit it with: nano .env"
        read -p "Press Enter after updating your API key..."
    else
        echo "❌ env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import fastapi, streamlit, langgraph" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🚀 Starting ISO 27001:2022 Auditor Agent..."
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped"
    fi
    echo "👋 Goodbye!"
    exit 0
}

# Set trap for cleanup on script exit
trap cleanup SIGINT SIGTERM EXIT

# Start backend
echo "🔌 Starting FastAPI backend..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✅ Backend started successfully on http://localhost:8000"

# Start frontend
echo "🎨 Starting Streamlit frontend..."
cd frontend
streamlit run app.py --server.port 8501 --server.headless true &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend started successfully on http://localhost:8501"

echo ""
echo "🎉 Application started successfully!"
echo "📱 Frontend: http://localhost:8501"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running and monitor processes
while true; do
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend process stopped unexpectedly"
        break
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend process stopped unexpectedly"
        break
    fi
    
    sleep 2
done

cleanup
