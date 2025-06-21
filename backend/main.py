from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from datetime import datetime
from typing import Dict, Any
import uvicorn

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

# Create FastAPI app
app = FastAPI(title="AI Dev Platform API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combine FastAPI and Socket.IO
socket_app = socketio.ASGIApp(sio, app)

@app.get("/")
async def root():
    return {"message": "AI Dev Platform API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")
    await sio.emit('connected', {'status': 'Connected to server'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
async def message(sid, data: Dict[str, Any]):
    """Handle incoming messages and broadcast to all clients"""
    try:
        # Validate message structure
        required_fields = ['userId', 'role', 'text']
        if not all(field in data for field in required_fields):
            await sio.emit('error', {
                'message': 'Invalid message format. Required fields: userId, role, text'
            }, room=sid)
            return

        # Add timestamp if not provided
        if 'ts' not in data:
            data['ts'] = datetime.utcnow().isoformat()

        # Broadcast message to all connected clients in /ws namespace
        await sio.emit('message', data)
        print(f"Message from {data['userId']} ({data['role']}): {data['text']}")
        
    except Exception as e:
        print(f"Error handling message: {str(e)}")
        await sio.emit('error', {'message': 'Error processing message'}, room=sid)

@sio.event
async def join_room(sid, data):
    """Allow clients to join specific rooms (future feature)"""
    room = data.get('room', 'general')
    await sio.enter_room(sid, room)
    await sio.emit('joined_room', {'room': room}, room=sid)

if __name__ == "__main__":
    uvicorn.run("main:socket_app", host="0.0.0.0", port=8000, reload=True) 