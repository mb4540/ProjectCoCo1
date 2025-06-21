from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import socketio
from datetime import datetime
from typing import Dict, Any, List
import uvicorn
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

# Create FastAPI app
app = FastAPI(title="AI Dev Platform API", version="1.0.0")

# Pydantic models for API
class Message(BaseModel):
    userId: str
    role: str
    text: str
    ts: str

class AgentReplyRequest(BaseModel):
    transcript: List[Message]
    role: str = "assistant"

class AgentReplyResponse(BaseModel):
    message: Message

# Store recent messages for context
recent_messages: List[Dict[str, Any]] = []

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

@app.post("/agent/reply", response_model=AgentReplyResponse)
async def agent_reply(request: AgentReplyRequest):
    """Generate AI assistant response based on chat transcript"""
    if not openai_client:
        raise HTTPException(status_code=503, detail="OpenAI API key not configured")
    
    try:
        # Convert transcript to OpenAI chat format
        messages = []
        for msg in request.transcript[-10:]:  # Last 10 messages
            role = "assistant" if msg.userId == "assistant" else "user"
            content = f"[{msg.role}] {msg.userId}: {msg.text}"
            messages.append({"role": role, "content": content})
        
        # Add system message
        system_message = {
            "role": "system", 
            "content": "You are a helpful AI assistant in a development platform. Respond concisely and helpfully to questions and discussions."
        }
        messages.insert(0, system_message)
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        # Create response message
        assistant_message = Message(
            userId="assistant",
            role=request.role,
            text=response.choices[0].message.content.strip(),
            ts=datetime.utcnow().isoformat()
        )
        
        return AgentReplyResponse(message=assistant_message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

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

        # Store message for context
        recent_messages.append(data)
        # Keep only last 50 messages
        if len(recent_messages) > 50:
            recent_messages.pop(0)

        # Broadcast message to all connected clients
        await sio.emit('message', data)
        print(f"Message from {data['userId']} ({data['role']}): {data['text']}")
        
        # Check if message mentions @Assistant and trigger AI response
        if "@Assistant" in data['text'] and openai_client and data['userId'] != 'assistant':
            try:
                # Prepare transcript from recent messages
                transcript = [Message(**msg) for msg in recent_messages[-10:]]
                
                # Create request
                request = AgentReplyRequest(transcript=transcript, role="assistant")
                
                # Get AI response
                response = await agent_reply(request)
                
                # Broadcast AI response
                assistant_data = response.message.dict()
                recent_messages.append(assistant_data)
                await sio.emit('message', assistant_data)
                print(f"AI Assistant responded: {assistant_data['text'][:100]}...")
                
            except Exception as e:
                print(f"Error generating AI response: {str(e)}")
                # Send error message as assistant
                error_message = {
                    'userId': 'assistant',
                    'role': 'assistant',
                    'text': 'Sorry, I encountered an error while processing your request.',
                    'ts': datetime.utcnow().isoformat()
                }
                await sio.emit('message', error_message)
        
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