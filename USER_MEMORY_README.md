# User Memory System for ISO 27001:2022 Auditor Agent

## Overview

The ISO 27001:2022 Auditor Agent now includes a comprehensive user memory system that provides personalized conversation history, learning progress tracking, and session management for each authenticated user.

## Features

### 🔐 User-Specific Memory
- **Persistent Storage**: All conversations are stored in a database linked to specific users
- **Session Management**: Users can have multiple conversation sessions
- **Context Awareness**: The agent remembers previous conversations within each session
- **Cross-Session Learning**: Learning progress is tracked across all user sessions

### 📊 Learning Progress Tracking
- **Learning Levels**: Beginner, Intermediate, Advanced based on conversation topics
- **Topic Coverage**: Tracks which ISO 27001:2022 topics have been discussed
- **Progress Analytics**: Provides insights into user's learning journey
- **Smart Suggestions**: Recommends next steps based on current knowledge

### 🗂️ Session Management
- **Multiple Sessions**: Users can create new conversations while preserving old ones
- **Session History**: Complete conversation history for each session
- **Session Summary**: AI-generated summaries of session content and focus areas
- **Session Deletion**: Users can clean up old sessions

## Architecture

### Database Models

#### User Model
```python
class User(Base):
    id: Primary key
    name: User's full name
    email: Unique email address
    organization_name: Company/organization
    domain: Industry domain
    location: Geographic location
    password_hash: Encrypted password
    created_at: Account creation timestamp
    updated_at: Last update timestamp
    conversations: Relationship to UserConversation
```

#### UserConversation Model
```python
class UserConversation(Base):
    id: Primary key
    user_id: Foreign key to User
    session_id: Unique session identifier
    query: User's question
    response: Agent's response
    timestamp: When the exchange occurred
    user: Relationship to User
```

### Service Layer

#### UserConversationService
- **store_conversation()**: Saves new conversation exchanges
- **get_user_conversations()**: Retrieves user's conversation history
- **get_session_conversations()**: Gets conversations for a specific session
- **create_user_memory()**: Creates LangChain memory with user context
- **get_user_conversation_summary()**: Analyzes conversation topics and focus
- **get_user_learning_progress()**: Tracks learning progress and suggests next steps
- **delete_user_session()**: Removes session data

## API Endpoints

### Core Chat Endpoint
```
POST /query
- Requires: JWT authentication
- Stores: User query and agent response
- Returns: Response with conversation history
- Features: Automatic session management
```

### Session Management
```
GET /sessions - List user's conversation sessions
GET /session/{session_id}/history - Get session conversation history
DELETE /session/{session_id} - Delete a session
```

### User Analytics
```
GET /user/progress - Get learning progress and topic coverage
GET /user/sessions/{session_id}/summary - Get session analysis
```

## Frontend Integration

### New Features Added
- **Progress Dashboard**: Shows learning level and topics covered
- **Session Browser**: Lists all user sessions with message counts
- **Active Session Indicator**: Shows current session information
- **Enhanced Sidebar**: Quick access to progress and session management

### User Experience Improvements
- **Persistent Memory**: Conversations continue seamlessly across page refreshes
- **Learning Insights**: Users can see their progress and get recommendations
- **Session Control**: Easy management of multiple conversation threads
- **Visual Feedback**: Clear indication of active sessions and progress

## Setup Instructions

### 1. Database Setup
```bash
cd backend
python setup_user_memory.py
```

### 2. Start Services
```bash
# Terminal 1: Start authentication service
cd backend
python login.py

# Terminal 2: Start main agent service
cd backend
python main.py

# Terminal 3: Start frontend
cd frontend
streamlit run app_with_auth.py
```

### 3. Test the System
```bash
cd backend
python test_user_memory.py
```

## Usage Examples

### Creating a New Conversation
1. Login to the system
2. Type your first question about ISO 27001:2022
3. The system automatically creates a new session
4. Continue asking follow-up questions in the same session

### Starting a New Session
1. Click "🆕 New Conversation" in the sidebar
2. Ask a new question
3. A new session is created while preserving the old one

### Checking Your Progress
1. Click "📊 Show My Progress" in the sidebar
2. View your learning level and topics covered
3. See suggested next steps for continued learning

### Managing Sessions
1. Click "📋 My Sessions" to see all your conversations
2. View message counts and creation dates
3. Delete old sessions if needed

## Technical Details

### Memory Implementation
- **LangChain Integration**: Uses ConversationBufferWindowMemory for context
- **Database Persistence**: All conversations stored in PostgreSQL
- **User Isolation**: Complete separation between different users' data
- **Session Scoping**: Memory context limited to specific sessions

### Performance Considerations
- **Memory Window**: Limited to last 20 exchanges per session
- **Database Indexing**: Optimized queries with proper indexes
- **Lazy Loading**: Memory loaded only when needed
- **Efficient Queries**: Minimal database calls for optimal performance

### Security Features
- **JWT Authentication**: Secure user identification
- **User Isolation**: Users can only access their own data
- **Input Validation**: All user inputs are validated and sanitized
- **Session Security**: Session IDs are UUID-based and secure

## Troubleshooting

### Common Issues

#### Database Connection Errors
- Check PostgreSQL service is running
- Verify database credentials in `.env` file
- Ensure database exists and is accessible

#### Memory Not Persisting
- Verify database tables were created
- Check user authentication is working
- Ensure conversation service is properly initialized

#### Session Management Issues
- Clear browser cache and cookies
- Check if JWT token is valid
- Verify backend services are running

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

## Future Enhancements

### Planned Features
- **Advanced Analytics**: Detailed learning path recommendations
- **Collaborative Learning**: Share insights between team members
- **Export Functionality**: Download conversation history and progress reports
- **Integration APIs**: Connect with external learning management systems

### Performance Improvements
- **Caching Layer**: Redis-based conversation caching
- **Async Processing**: Background conversation analysis
- **Smart Summarization**: AI-powered conversation summaries
- **Predictive Suggestions**: Proactive learning recommendations

## Contributing

To contribute to the user memory system:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For questions or issues with the user memory system:

1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
4. Contact the development team

---

**Note**: This user memory system is designed to enhance the learning experience while maintaining user privacy and data security. All conversations are stored securely and are only accessible to the authenticated user who created them.
