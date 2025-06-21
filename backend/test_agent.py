import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
from main import app, Message, AgentReplyRequest

client = TestClient(app)

@pytest.fixture
def sample_transcript():
    """Sample chat transcript for testing"""
    return [
        Message(
            userId="user1",
            role="developer",
            text="Hello there!",
            ts="2024-01-01T10:00:00.000Z"
        ),
        Message(
            userId="user2", 
            role="developer",
            text="How can I help with the project?",
            ts="2024-01-01T10:01:00.000Z"
        ),
        Message(
            userId="user1",
            role="developer", 
            text="@Assistant Can you explain this code?",
            ts="2024-01-01T10:02:00.000Z"
        )
    ]

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_agent_reply_no_api_key():
    """Test agent reply without OpenAI API key"""
    with patch.dict(os.environ, {}, clear=True):
        # Reload the module to reset openai_client
        import importlib
        import main
        importlib.reload(main)
        
        from main import app
        test_client = TestClient(app)
        
        request_data = {
            "transcript": [
                {
                    "userId": "user1",
                    "role": "developer",
                    "text": "Hello",
                    "ts": "2024-01-01T10:00:00.000Z"
                }
            ],
            "role": "assistant"
        }
        
        response = test_client.post("/agent/reply", json=request_data)
        assert response.status_code == 503
        assert "OpenAI API key not configured" in response.json()["detail"]

@patch('main.openai_client')
def test_agent_reply_with_api_key(mock_client, sample_transcript):
    """Test agent reply with mocked OpenAI API"""
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a helpful AI response about the code."
    mock_client.chat.completions.create.return_value = mock_response
    
    # Ensure mock_client is truthy
    mock_client.__bool__ = lambda self: True
    
    request_data = {
        "transcript": [msg.dict() for msg in sample_transcript],
        "role": "assistant"
    }
    
    response = client.post("/agent/reply", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert data["message"]["userId"] == "assistant"
    assert data["message"]["role"] == "assistant"
    assert data["message"]["text"] == "This is a helpful AI response about the code."
    assert len(data["message"]["text"]) > 0
    assert "ts" in data["message"]
    
    # Verify OpenAI was called with correct parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args
    assert call_args[1]["model"] == "gpt-3.5-turbo"
    assert call_args[1]["max_tokens"] == 500
    assert call_args[1]["temperature"] == 0.7
    assert len(call_args[1]["messages"]) == 4  # 1 system + 3 transcript messages

@patch('main.openai_client')
def test_agent_reply_openai_error(mock_client, sample_transcript):
    """Test agent reply when OpenAI API fails"""
    # Mock OpenAI to raise an exception
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_client.__bool__ = lambda self: True
    
    request_data = {
        "transcript": [msg.dict() for msg in sample_transcript],
        "role": "assistant"
    }
    
    response = client.post("/agent/reply", json=request_data)
    assert response.status_code == 500
    assert "Error generating response" in response.json()["detail"]

def test_agent_reply_invalid_request():
    """Test agent reply with invalid request format"""
    request_data = {
        "transcript": "invalid format",  # Should be a list
        "role": "assistant"
    }
    
    response = client.post("/agent/reply", json=request_data)
    assert response.status_code == 422  # Validation error

@patch('main.openai_client')
def test_agent_reply_limits_transcript(mock_client):
    """Test that agent reply limits transcript to last 10 messages"""
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "AI response"
    mock_client.chat.completions.create.return_value = mock_response
    mock_client.__bool__ = lambda self: True
    
    # Create 15 messages
    transcript = []
    for i in range(15):
        transcript.append({
            "userId": f"user{i}",
            "role": "developer",
            "text": f"Message {i}",
            "ts": f"2024-01-01T10:{i:02d}:00.000Z"
        })
    
    request_data = {
        "transcript": transcript,
        "role": "assistant"
    }
    
    response = client.post("/agent/reply", json=request_data)
    assert response.status_code == 200
    
    # Verify OpenAI was called with only 11 messages (1 system + 10 transcript)
    call_args = mock_client.chat.completions.create.call_args
    assert len(call_args[1]["messages"]) == 11

if __name__ == "__main__":
    pytest.main([__file__])