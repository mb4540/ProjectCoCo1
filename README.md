# AI Dev Platform

A modern AI-assisted development platform built with React/TypeScript frontend and FastAPI/Python backend, featuring real-time chat communication via Socket.IO.

## Features

- **Real-time Chat**: WebSocket-based communication using Socket.IO
- **Modern UI**: Clean, responsive interface with dark/light theme support
- **TypeScript**: Full type safety across the application
- **Containerized**: Docker-based development environment
- **Role-based Messaging**: Support for different user roles (developer, admin, AI, user)
- **Message History**: Persistent chat history during session

## Tech Stack

### Frontend
- **Vite** - Fast build tool and dev server
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Socket.IO Client** - Real-time WebSocket communication
- **Lucide React** - Beautiful, customizable icons

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Socket.IO** - Real-time bidirectional communication
- **Python 3.12** - Latest Python features
- **Uvicorn** - ASGI server

### DevOps
- **Docker & Docker Compose** - Containerized development
- **Hot Reload** - Both frontend and backend support live reloading

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProjectCoCo1
   ```

2. **Start the application**
   ```bash
   docker compose up
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Git

### Environment Configuration

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Modify `.env` as needed (optional for development)

### Running the Application

**Option 1: Docker Compose (Recommended)**
```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Rebuild and start
docker compose up --build
```

**Option 2: Local Development**

*Backend:*
```bash
cd backend
pip install -r requirements.txt
uvicorn main:socket_app --host 0.0.0.0 --port 8000 --reload
```

*Frontend:*
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
ProjectCoCo1/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatPage.tsx
│   │   │   ├── MessageItem.tsx
│   │   │   └── *.css
│   │   ├── hooks/          # Custom React hooks
│   │   │   └── useSocket.ts
│   │   ├── types/          # TypeScript type definitions
│   │   │   └── message.ts
│   │   ├── App.tsx         # Main App component
│   │   └── main.tsx        # Application entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── backend/                  # FastAPI Python backend
│   ├── main.py              # FastAPI application with Socket.IO
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── docker-compose.yml       # Docker services configuration
├── env.example             # Environment variables template
└── README.md               # This file
```

## API Endpoints

### HTTP Endpoints
- `GET /` - Basic API status
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger)

### Socket.IO Events

**Client → Server:**
- `message` - Send a chat message
  ```json
  {
    "userId": "string",
    "role": "string", 
    "text": "string",
    "ts": "ISO timestamp (optional)"
  }
  ```

**Server → Client:**
- `connected` - Connection confirmation
- `message` - Broadcast message to all clients
- `error` - Error notifications

## Usage Examples

### Sending Messages

The chat interface automatically sends messages with the following structure:
```json
{
  "userId": "user_abc123",
  "role": "developer",
  "text": "Hello, world!",
  "ts": "2024-01-01T12:00:00.000Z"
}
```

### Role Types

The platform supports different user roles:
- `developer` - Development team members (blue badge)
- `admin` - Administrators (red badge)  
- `ai` - AI assistants (purple badge)
- `user` - General users (green badge)

## Development

### Adding New Features

1. **Frontend Changes**: Modify components in `frontend/src/components/`
2. **Backend Changes**: Update `backend/main.py` for new endpoints or Socket.IO events
3. **Styling**: Update CSS files in component directories

### Hot Reloading

Both frontend and backend support hot reloading:
- Frontend: Vite automatically reloads on file changes
- Backend: Uvicorn reloads on Python file changes

### Debugging

**View Application Logs:**
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f frontend
docker compose logs -f backend
```

**Access Container Shell:**
```bash
# Frontend container
docker compose exec frontend sh

# Backend container  
docker compose exec backend bash
```

## Production Deployment

For production deployment, you'll want to:

1. **Build optimized frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Use production Docker images**
3. **Set environment variables for production**
4. **Configure reverse proxy (nginx)**
5. **Set up SSL certificates**
6. **Configure persistent storage if needed**

## Troubleshooting

**Common Issues:**

1. **Port already in use:**
   ```bash
   # Check what's using the port
   sudo lsof -i :3000
   sudo lsof -i :8000
   
   # Kill the process or change ports in docker-compose.yml
   ```

2. **Docker build failures:**
   ```bash
   # Clean rebuild
   docker compose down
   docker compose build --no-cache
   docker compose up
   ```

3. **Socket.IO connection issues:**
   - Check that backend is running on port 8000
   - Verify CORS settings in FastAPI
   - Check browser developer tools for WebSocket errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 