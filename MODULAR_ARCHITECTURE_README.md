# Modular Architecture for ISO 27001:2022 Auditor Agent

## Overview

The backend has been refactored into a clean, modular architecture that separates concerns and makes the codebase more maintainable and scalable.

## File Structure

```
backend/
├── main.py                 # Main FastAPI application entry point
├── dependencies.py         # Shared dependencies and utilities
├── knowledge_base.py       # ISO 27001:2022 knowledge base
├── agent_graph.py          # LangGraph agent workflow and logic
├── api_routes.py           # API route handlers and business logic
├── conversation_service.py  # User conversation and memory management
├── models.py               # Database models
├── database.py             # Database configuration and connection
├── auth.py                 # Authentication utilities
└── login.py                # Authentication service
```

## Architecture Components

### 1. **main.py** - Application Entry Point
- **Purpose**: Main FastAPI application configuration and orchestration
- **Responsibilities**:
  - Create and configure FastAPI app
  - Set up middleware (CORS, etc.)
  - Include API routes
  - Define root endpoints
- **Size**: ~50 lines (down from ~600 lines)

### 2. **dependencies.py** - Shared Dependencies
- **Purpose**: Centralized dependency injection and utilities
- **Contents**:
  - JWT authentication dependency (`get_current_user`)
  - OpenAI model factory (`get_llm`)
  - Security schemes and utilities
- **Benefits**: Single source of truth for dependencies

### 3. **knowledge_base.py** - ISO 27001:2022 Knowledge
- **Purpose**: Centralized knowledge base for the auditor agent
- **Contents**:
  - Standard overview and key changes
  - Control groups and specific controls
  - Implementation steps and benefits
- **Benefits**: Easy to maintain and update knowledge base

### 4. **agent_graph.py** - Agent Workflow Logic
- **Purpose**: LangGraph workflow and agent state management
- **Contents**:
  - `AgentState` model definition
  - `iso_27001_auditor_node` function
  - Graph creation and compilation
  - Memory integration logic
- **Benefits**: Isolated agent logic, easier testing

### 5. **api_routes.py** - API Endpoints
- **Purpose**: All API route handlers and business logic
- **Contents**:
  - Query processing endpoint
  - Session management endpoints
  - User progress and analytics endpoints
  - Health check endpoints
- **Benefits**: Clean separation of API logic

### 6. **conversation_service.py** - User Memory Management
- **Purpose**: Service layer for user conversations and memory
- **Contents**:
  - Conversation storage and retrieval
  - Memory creation and management
  - Learning progress tracking
  - Session analytics
- **Benefits**: Reusable service layer

## Benefits of the New Architecture

### 🔧 **Maintainability**
- **Single Responsibility**: Each file has a clear, focused purpose
- **Easy Navigation**: Developers can quickly find specific functionality
- **Reduced Complexity**: Smaller, focused files are easier to understand

### 🚀 **Scalability**
- **Modular Growth**: New features can be added to appropriate modules
- **Independent Development**: Teams can work on different modules simultaneously
- **Clear Interfaces**: Well-defined boundaries between components

### 🧪 **Testing**
- **Isolated Testing**: Each module can be tested independently
- **Mock Dependencies**: Easy to mock dependencies for unit tests
- **Focused Test Suites**: Tests can target specific functionality

### 🔄 **Reusability**
- **Shared Components**: Dependencies and utilities are easily shared
- **Service Layer**: Business logic can be reused across different endpoints
- **Knowledge Base**: Centralized knowledge can be used by multiple agents

## API Structure

### Base URL
```
http://localhost:8000/api/v1
```

### Available Endpoints
- `POST /query` - Process ISO 27001:2022 compliance queries
- `GET /sessions` - List user's conversation sessions
- `GET /session/{id}/history` - Get session conversation history
- `DELETE /session/{id}` - Delete a session
- `GET /user/progress` - Get user's learning progress
- `GET /user/sessions/{id}/summary` - Get session summary
- `GET /health` - Health check

## Development Workflow

### Adding New Features
1. **New API Endpoints**: Add to `api_routes.py`
2. **New Agent Logic**: Add to `agent_graph.py`
3. **New Knowledge**: Add to `knowledge_base.py`
4. **New Dependencies**: Add to `dependencies.py`

### Modifying Existing Features
1. **API Changes**: Modify `api_routes.py`
2. **Agent Changes**: Modify `agent_graph.py`
3. **Knowledge Updates**: Modify `knowledge_base.py`
4. **Dependency Changes**: Modify `dependencies.py`

## Migration Notes

### What Changed
- **main.py**: Reduced from ~600 lines to ~50 lines
- **Code Organization**: Logic moved to appropriate modules
- **Import Structure**: Updated imports to use new modules
- **API Routes**: Now prefixed with `/api/v1`

### What Stayed the Same
- **Functionality**: All features remain unchanged
- **Database Models**: No changes to data structure
- **User Experience**: Frontend continues to work as before
- **API Responses**: Same response format and structure

## Testing the New Architecture

### 1. **Test Individual Modules**
```bash
# Test knowledge base
python -c "from knowledge_base import ISO_27001_KNOWLEDGE; print('Knowledge base loaded successfully')"

# Test agent graph
python -c "from agent_graph import app_state; print('Agent graph compiled successfully')"

# Test dependencies
python -c "from dependencies import get_llm; print('Dependencies loaded successfully')"
```

### 2. **Test API Routes**
```bash
# Start the application
python main.py

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

### 3. **Test Full System**
```bash
# Run the demo
python demo_user_memory.py

# Test with frontend
streamlit run frontend/app_with_auth.py
```

## Future Enhancements

### Planned Improvements
- **Configuration Management**: Separate config files for different environments
- **Logging**: Centralized logging configuration
- **Error Handling**: Standardized error handling across modules
- **Validation**: Centralized request/response validation
- **Documentation**: Auto-generated API documentation

### Potential Extensions
- **Multiple Agents**: Easy to add new agent types
- **Plugin System**: Modular knowledge base extensions
- **API Versioning**: Clean API version management
- **Microservices**: Easy to split into separate services

## Conclusion

The new modular architecture provides:
- ✅ **Better Organization**: Clear separation of concerns
- ✅ **Easier Maintenance**: Focused, manageable files
- ✅ **Improved Testing**: Isolated, testable components
- ✅ **Enhanced Scalability**: Easy to extend and modify
- ✅ **Better Developer Experience**: Clear file structure and purpose

This architecture makes the codebase more professional, maintainable, and ready for future growth while preserving all existing functionality.
