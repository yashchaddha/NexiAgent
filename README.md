# 🔒 ISO 27001:2022 Auditor Agent

An intelligent agent built with LangGraph, FastAPI, and Streamlit that acts as an expert Internal Auditor for ISO 27001:2022 compliance framework. The agent provides comprehensive guidance on information security management systems, control implementation, and compliance best practices.

## 🏗️ Architecture

- **Backend**: FastAPI with LangGraph StateGraph
- **Frontend**: Streamlit with modern chat interface
- **AI Engine**: OpenAI GPT-4 with ISO 27001:2022 knowledge base
- **State Management**: Single-node LangGraph workflow

## ✨ Features

- **Expert Knowledge**: Comprehensive understanding of ISO 27001:2022 standard
- **Interactive Chat**: User-friendly chat interface for compliance queries
- **Real-time Responses**: Instant answers to ISO compliance questions
- **Control Guidance**: Detailed information on all 93 controls
- **Implementation Support**: Step-by-step guidance for compliance projects
- **Risk Assessment**: Expert advice on security risk management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd completeAgent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Start the backend**
   ```bash
   cd backend
   python main.py
   ```

5. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```

6. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

## 📁 Project Structure

```
completeAgent/
├── backend/
│   └── main.py              # FastAPI backend with LangGraph
├── frontend/
│   └── app.py               # Streamlit UI
├── requirements.txt          # Python dependencies
├── env.example              # Environment variables template
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=8501
```

### API Configuration

The frontend connects to the backend API. You can modify the API URL in the Streamlit sidebar if needed.

## 💬 Usage Examples

### Sample Queries

- "What are the main control groups in ISO 27001:2022?"
- "How do I implement access control policies?"
- "What is the risk assessment process?"
- "Explain control A.5.1 - Information security policies"
- "How do I conduct an internal audit?"
- "What are the key changes in the 2022 version?"

### Quick Actions

The sidebar includes quick action buttons for common queries:
- 📋 Show Control Groups
- 🔍 Risk Assessment
- 📚 Implementation Steps

## 🧠 Knowledge Base

The agent includes comprehensive knowledge of:

- **Control Groups**: People, Organizational, Technological, Physical
- **Specific Controls**: All 93 controls with descriptions
- **Implementation Steps**: 6-step process for ISMS implementation
- **Best Practices**: Industry-standard compliance approaches
- **Risk Management**: Assessment and treatment methodologies

## 🔌 API Endpoints

### Backend API

- `GET /` - Root endpoint
- `POST /query` - Process ISO compliance queries
- `GET /health` - Health check

### Request/Response Format

```json
POST /query
{
  "query": "How do I implement ISO 27001:2022?"
}

Response:
{
  "response": "Detailed implementation guidance...",
  "query": "How do I implement ISO 27001:2022?"
}
```

## 🛠️ Development

### Running in Development Mode

1. **Backend Development**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   streamlit run app.py --server.port 8501
   ```

### Testing

Test the API connection using the "Test Connection" button in the Streamlit sidebar.

## 📚 ISO 27001:2022 Information

### Key Changes in 2022 Version

- Reduced from 114 controls to 93 controls
- Reorganized into 4 control groups instead of 14
- New controls for cloud security and threat intelligence
- Enhanced focus on data protection and privacy

### Control Groups

1. **People (A.7)**: Human resource security, awareness, and training
2. **Organizational (A.5)**: Policies, procedures, and organizational structure
3. **Technological (A.8)**: Technical controls for systems and infrastructure
4. **Physical (A.6)**: Physical security controls for facilities and equipment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool provides guidance based on ISO 27001:2022 standards but should not replace professional consultation. Always refer to official ISO documentation and consult with qualified professionals for compliance matters.

## 🆘 Support

For issues and questions:
1. Check the API connection in the sidebar
2. Verify your OpenAI API key is set correctly
3. Ensure both backend and frontend are running
4. Check the console for error messages

## 🔗 Useful Links

- [ISO 27001:2022 Official Standard](https://www.iso.org/standard/27001)
- [ISO 27001 Information Security Management](https://www.iso.org/isoiec-27001-information-security)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
