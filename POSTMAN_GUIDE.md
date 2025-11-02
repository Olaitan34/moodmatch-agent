# MoodMatch Agent - Postman Testing Guide

## 🚀 Quick Start

**Server URL:** `http://localhost:8000`

Start server: `python main.py`

---

## 📋 Table of Contents

1. [Health Check](#1-health-check)
2. [Execute Method - Get Recommendations](#2-execute-method---get-recommendations)
3. [Message/Send Method - Send Message](#3-messagesend-method---send-message)
4. [Example Test Scenarios](#4-example-test-scenarios)
5. [Response Structure](#5-response-structure)
6. [Error Handling](#6-error-handling)

---

## 1. Health Check

### Check if server is running

**Method:** `GET`  
**URL:** `http://localhost:8000/health`  
**Headers:** None required

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "MoodMatch A2A Agent",
  "version": "1.0.0"
}
```

---

## 2. Execute Method - Get Recommendations

### Get mood-based recommendations (music, movies, books)

This is the **MAIN** endpoint - use this to get personalized recommendations!

**Method:** `POST`  
**URL:** `http://localhost:8000/a2a/moodmatch`  
**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "I'm feeling stressed and overwhelmed with work"
          }
        ]
      }
    ]
  }
}
```

**Success Response (200 OK):**
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "result": {
    "taskId": "unique-task-id",
    "contextId": "unique-context-id",
    "status": {
      "state": "completed",
      "timestamp": "2025-11-02T12:00:00",
      "message": "Task completed successfully"
    },
    "artifacts": [
      {
        "kind": "data",
        "data": {
          "mood": {
            "primary_mood": "stressed",
            "intensity": 7,
            "context": "work-related stress"
          }
        },
        "name": "Mood Analysis",
        "description": "Your detected mood"
      },
      {
        "kind": "data",
        "data": {
          "playlist_name": "Stress Relief",
          "tracks": [...],
          "total_tracks": 20
        },
        "name": "Music Recommendation",
        "description": "Curated playlist for stress relief"
      },
      {
        "kind": "data",
        "data": {
          "title": "The Grand Budapest Hotel",
          "genres": ["Comedy", "Drama"],
          "rating": 8.1
        },
        "name": "Movie Recommendation",
        "description": "Uplifting movie recommendation"
      },
      {
        "kind": "data",
        "data": {
          "title": "The Subtle Art of Not Giving a F*ck",
          "authors": ["Mark Manson"],
          "description": "A counterintuitive approach to living a good life"
        },
        "name": "Book Recommendation",
        "description": "Book to help manage stress"
      }
    ],
    "history": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "I'm feeling stressed and overwhelmed with work"
          }
        ],
        "timestamp": "2025-11-02T12:00:00"
      },
      {
        "role": "agent",
        "parts": [
          {
            "kind": "text",
            "text": "I understand you're feeling stressed. Here are some personalized recommendations..."
          }
        ],
        "timestamp": "2025-11-02T12:00:01"
      }
    ],
    "kind": "task",
    "metadata": {},
    "createdAt": "2025-11-02T12:00:00"
  }
}
```

---

## 3. Message/Send Method - Send Message

### Send a message without expecting full recommendations

**Method:** `POST`  
**URL:** `http://localhost:8000/a2a/moodmatch`  
**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "jsonrpc": "2.0",
  "id": "msg-456",
  "method": "message/send",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "How are you?"
          }
        ]
      }
    ]
  }
}
```

**Success Response (200 OK):**
```json
{
  "jsonrpc": "2.0",
  "id": "msg-456",
  "result": {
    "taskId": "unique-task-id",
    "contextId": "unique-context-id",
    "status": {
      "state": "completed",
      "timestamp": "2025-11-02T12:00:00"
    },
    "artifacts": [],
    "history": [
      {
        "role": "agent",
        "parts": [
          {
            "kind": "text",
            "text": "I'm doing well! How can I help you today?"
          }
        ]
      }
    ],
    "kind": "task",
    "metadata": {},
    "createdAt": "2025-11-02T12:00:00"
  }
}
```

---

## 4. Example Test Scenarios

### Scenario 1: Happy Mood
```json
{
  "jsonrpc": "2.0",
  "id": "happy-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "I'm so happy! Just got promoted at work!"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Upbeat music, feel-good movies, motivational books

---

### Scenario 2: Sad/Lonely Mood
```json
{
  "jsonrpc": "2.0",
  "id": "sad-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Feeling down and lonely tonight"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Comforting music, heartwarming movies, uplifting books

---

### Scenario 3: Anxious Mood
```json
{
  "jsonrpc": "2.0",
  "id": "anxious-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "I'm worried about my exam tomorrow"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Calming music, light movies, self-help books

---

### Scenario 4: Energetic/Excited Mood
```json
{
  "jsonrpc": "2.0",
  "id": "energetic-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "I'm pumped! Ready to conquer the day!"
          }
        ]
      }
    ]
  }
}
```

**Expected:** High-energy music, action movies, adventure books

---

### Scenario 5: Tired/Burnt Out
```json
{
  "jsonrpc": "2.0",
  "id": "tired-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Exhausted from working overtime all week"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Relaxing music, easy-watch movies, light reading

---

### Scenario 6: Romantic Mood
```json
{
  "jsonrpc": "2.0",
  "id": "romantic-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Planning a special date night with my partner"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Romantic music, romance movies, love-themed books

---

### Scenario 7: Nostalgic Mood
```json
{
  "jsonrpc": "2.0",
  "id": "nostalgic-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Missing my childhood days and simpler times"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Classic songs, nostalgic movies, memoir books

---

### Scenario 8: Multi-Mood
```json
{
  "jsonrpc": "2.0",
  "id": "multi-mood-test",
  "method": "execute",
  "params": {
    "messages": [
      {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "I'm excited about my new job but also anxious about starting"
          }
        ]
      }
    ]
  }
}
```

**Expected:** Balanced recommendations addressing both excitement and anxiety

---

## 5. Response Structure

### Success Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `jsonrpc` | string | Always "2.0" |
| `id` | string/int | Same as request ID |
| `result.taskId` | string | Unique task identifier |
| `result.contextId` | string | Conversation context ID |
| `result.status.state` | string | "completed", "failed", "working" |
| `result.artifacts` | array | Mood analysis and recommendations |
| `result.history` | array | Conversation history |
| `result.kind` | string | Always "task" |

### Artifact Types

1. **Mood Analysis Artifact**
   - Contains: primary_mood, intensity, context, immediate_need
   - Shows detected emotional state

2. **Music Recommendation Artifact**
   - Contains: playlist_name, tracks, artists, genres
   - Spotify-based recommendations

3. **Movie Recommendation Artifact**
   - Contains: title, genres, overview, rating
   - TMDB-based recommendations

4. **Book Recommendation Artifact**
   - Contains: title, authors, description, categories
   - Google Books-based recommendations

---

## 6. Error Handling

### Invalid Request (400 Bad Request)
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "error": {
    "code": -32600,
    "message": "Invalid Request: Missing required field 'method'"
  }
}
```

### Method Not Found (404)
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "error": {
    "code": -32601,
    "message": "Method not found: unknown_method"
  }
}
```

### Internal Server Error (500)
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "error": {
    "code": -32603,
    "message": "Internal server error: [error details]"
  }
}
```

### Failed Task Response
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "result": {
    "taskId": "unique-task-id",
    "status": {
      "state": "failed",
      "message": "Failed to analyze mood: [error details]"
    },
    "artifacts": [],
    "history": [
      {
        "role": "agent",
        "parts": [
          {
            "kind": "text",
            "text": "I apologize, but I encountered an issue: [error message]"
          }
        ]
      }
    ]
  }
}
```

---

## 🎯 Supported Moods (52 Total)

### Positive Emotions (10)
happy, excited, grateful, peaceful, confident, inspired, playful, content, loving, proud

### Negative Emotions (12)
sad, anxious, stressed, angry, lonely, heartbroken, disappointed, guilty, jealous, embarrassed, afraid, hopeless

### Energy States (8)
energetic, tired, restless, sluggish, hyper, burnt_out, mellow, drowsy

### Social/Relational (8)
social, introverted, romantic, nostalgic, homesick, misunderstood, betrayed, supported

### Existential/Reflective (8)
contemplative, philosophical, curious, confused, stuck, purposeful, empty, overwhelmed

### Transitional/Complex (6)
bittersweet, numb, vengeful, rebellious, vulnerable, bored

---

## 🔧 Testing Tips

1. **Use descriptive IDs** - Makes debugging easier
2. **Test with context** - "I'm stressed because of work deadlines"
3. **Try edge cases** - Empty messages, very long messages
4. **Test multi-mood** - "I'm happy but also nervous"
5. **Check conversation flow** - Send multiple messages in sequence

---

## 📊 Postman Collection Setup

### Create a New Collection

1. **Collection Name:** `MoodMatch Agent`
2. **Base URL Variable:** `{{base_url}}` = `http://localhost:8000`

### Add Requests

1. Health Check (GET)
2. Execute - Happy (POST)
3. Execute - Stressed (POST)
4. Execute - Sad (POST)
5. Execute - Energetic (POST)
6. Message Send (POST)

### Environment Variables

```
base_url = http://localhost:8000
request_id = {{$guid}}  (auto-generate unique IDs)
```

---

## 🚀 Quick Test Command (cURL Alternative)

For PowerShell users who prefer terminal:

```powershell
$body = @{
    jsonrpc = "2.0"
    id = "test-123"
    method = "execute"
    params = @{
        messages = @(
            @{
                role = "user"
                parts = @(
                    @{
                        kind = "text"
                        text = "I'm feeling happy today!"
                    }
                )
            }
        )
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8000/a2a/moodmatch" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 10
```

---

## ✅ Expected Results by Mood

| User Mood | Music Energy | Movie Genre | Book Type |
|-----------|-------------|-------------|-----------|
| Happy | High | Comedy, Romance | Feel-good Fiction |
| Sad | Low-Medium | Drama, Animation | Uplifting Stories |
| Stressed | Low | Light Comedy | Self-help, Relaxation |
| Energetic | Very High | Action, Adventure | Motivational, Thriller |
| Tired | Very Low | Light Drama | Easy Reading |
| Anxious | Low | Feel-good | Mindfulness, Calm |
| Romantic | Medium | Romance | Love Stories |
| Angry | High | Action, Thriller | Channel Energy |

---

## 🎉 Success Indicators

✅ Server responds within 5-10 seconds  
✅ Status is "completed"  
✅ Artifacts array has 4 items (mood + 3 recommendations)  
✅ Each recommendation has relevant data  
✅ Mood is mapped to one of the 52 valid moods  
✅ History shows both user and agent messages  

---

**Need Help?** Check server logs for detailed error messages!

**Server Logs Location:** Terminal where you ran `python main.py`
