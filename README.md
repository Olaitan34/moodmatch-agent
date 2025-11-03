# 🎭 MoodMatch A2A Agent

> **AI-powered mood analysis and personalized media recommendations via A2A protocol**

MoodMatch is an intelligent agent that understands your emotional state and recommends the perfect music, movies, and books to match or shift your mood. Built with Google's Gemini 2.0 Flash and integrated with Spotify, TMDB, and Google Books APIs.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![A2A Protocol](https://img.shields.io/badge/A2A-Protocol-orange.svg)](https://github.com/modelcontextprotocol/a2a-protocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Live Demo

- **Public Endpoint:** https://downier-virgulate-alanna.ngrok-free.dev/a2a/moodmatch
- **Health Check:** https://downier-virgulate-alanna.ngrok-free.dev/health
- **Telex.im Integration:** Available via A2A Protocol
- **Postman Guide:** [POSTMAN_GUIDE.md](./POSTMAN_GUIDE.md)

---

## ✨ Features

🧠 **Advanced Mood Analysis**
- Powered by Google Gemini 2.0 Flash (Experimental)
- 52 distinct mood classifications with intensity levels
- Contextual emotional understanding
- Multi-turn conversation support

🎵 **Personalized Music Recommendations**
- Spotify integration with intelligent search
- Mood-to-genre mapping
- Playlist and track recommendations
- Direct Spotify links

🎬 **Movie Recommendations**
- TMDB database access
- Genre-based discovery
- Streaming platform availability
- Ratings and detailed information

📚 **Book Recommendations**
- Google Books integration
- Quality filtering and curation
- Reading time estimates
- Preview links

🔌 **A2A Protocol Compliant**
- JSON-RPC 2.0 transport
- Full message/artifact support
- Context persistence
- Standard integration with A2A clients

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.13+ |
| **Web Framework** | FastAPI 0.115+ |
| **AI/LLM** | Pydantic AI 0.4+ with Google Gemini 2.0 Flash |
| **Music API** | Spotify Web API (via Spotipy 2.23+) |
| **Movie API** | The Movie Database (TMDB) API |
| **Books API** | Google Books API |
| **Protocol** | A2A (Agent-to-Agent) with JSON-RPC 2.0 |
| **HTTP Client** | HTTPX 0.28+ (async) |
| **Validation** | Pydantic v2 |

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.13+** installed
- API keys for the following services (all free!):
  - 🔑 Google Gemini API key
  - 🔑 TMDB API key
  - 🔑 Spotify Client ID & Secret
  - 🔑 Google Books API key (optional but recommended)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Olaitan34/moodmatch-agent.git
cd moodmatch-agent
```

### 2. Install Dependencies

Using pip:
```bash
pip install -e .
```

This will install all required packages from `pyproject.toml`:
- `fastapi[standard]>=0.115.12`
- `pydantic-ai>=0.4.2`
- `google-generativeai>=0.8.3`
- `spotipy>=2.23.0`
- `httpx>=0.28.1`
- `python-dotenv>=1.0.0`
- `uvicorn>=0.34.0`

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Google Gemini API (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# TMDB API (Required)
TMDB_API_KEY=your_tmdb_api_key_here

# Spotify API (Required)
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

# Google Books API (Optional)
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here

# Server Configuration
PORT=5001
```

### 4. Get API Keys

#### 🤖 Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your key
5. **Free tier**: 15 requests/minute, 1500 requests/day

#### 🎬 TMDB API
1. Visit [TMDB](https://www.themoviedb.org/settings/api)
2. Create an account
3. Request an API key (choose "Developer")
4. Copy your API key (v3 auth)
5. **Free tier**: 30 requests every 10 seconds

#### 🎵 Spotify API
1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Create an app
4. Copy Client ID and Client Secret
5. **Free tier**: No rate limits for basic API calls

#### 📚 Google Books API
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Books API"
4. Create credentials (API key)
5. **Free tier**: 1000 requests/day

---

## 🏃 Running the Agent

### Start the Server

```bash
python main.py
```

The server will start on `http://localhost:5001`

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     ✅ MoodMatch agent initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5001
```

### Access API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:5001/docs
- **Health Check**: http://localhost:5001/health

---

## 🧪 Testing the Agent

### Health Check

```bash
curl http://localhost:5001/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent": "MoodMatch A2A Agent",
  "version": "1.0.0",
  "agent_ready": true
}
```

### Send a Message (A2A Protocol)

```bash
curl -X POST http://localhost:5001/a2a/moodmatch \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-123",
    "method": "message/send",
    "params": {
      "messages": [
        {
          "role": "user",
          "parts": [
            {
              "type": "text",
              "text": "I'\''m feeling really stressed and overwhelmed with work. I need something to help me unwind."
            }
          ]
        }
      ]
    }
  }'
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "result": {
    "state": "completed",
    "messages": [
      {
        "role": "agent",
        "parts": [
          {
            "type": "text",
            "text": "I hear you... [empathetic response with recommendations]"
          }
        ]
      }
    ],
    "artifacts": [
      {
        "name": "mood_analysis",
        "description": "Detected mood and emotional context",
        "parts": [...]
      },
      {
        "name": "music_recommendation",
        "description": "Spotify music recommendation",
        "parts": [...]
      },
      {
        "name": "movie_recommendation",
        "description": "Movie recommendation from TMDB",
        "parts": [...]
      },
      {
        "name": "book_recommendation",
        "description": "Book recommendation from Google Books",
        "parts": [...]
      }
    ]
  }
}
```

---

## 🚀 Deployment

### Option 1: Railway

1. Fork this repository
2. Visit [Railway](https://railway.app/)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your fork
5. Add environment variables in Railway dashboard
6. Deploy!

Railway will automatically detect Python and install dependencies.

### Option 2: Render

1. Fork this repository
2. Visit [Render](https://render.com/)
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Set build command: `pip install -e .`
6. Set start command: `python main.py`
7. Add environment variables
8. Deploy!

### Option 3: Fly.io

1. Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
2. Login: `flyctl auth login`
3. Create `fly.toml`:

```toml
app = "moodmatch-agent"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

4. Set secrets:
```bash
flyctl secrets set GEMINI_API_KEY=your_key
flyctl secrets set TMDB_API_KEY=your_key
flyctl secrets set SPOTIFY_CLIENT_ID=your_id
flyctl secrets set SPOTIFY_CLIENT_SECRET=your_secret
flyctl secrets set GOOGLE_BOOKS_API_KEY=your_key
```

5. Deploy: `flyctl deploy`

---

## 🔌 A2A Protocol Integration

MoodMatch implements the [A2A Protocol](https://github.com/modelcontextprotocol/a2a-protocol) specification, making it compatible with any A2A client.

### Using with Telex

[Telex](https://github.com/modelcontextprotocol/telex) is a universal A2A client:

1. Install Telex (if not already installed)
2. Add MoodMatch to your Telex configuration:

```json
{
  "agents": [
    {
      "name": "MoodMatch",
      "url": "http://localhost:5001/a2a/moodmatch",
      "description": "Get mood-based music, movie, and book recommendations"
    }
  ]
}
```

3. Start chatting:
```
User: I'm feeling anxious about an upcoming presentation
Telex: [Routes to MoodMatch]
MoodMatch: I understand that pre-presentation anxiety... [recommendations]
```

### Integration with Other Agents

MoodMatch can be composed with other A2A agents:

```
User → Telex → [Your Task Agent] → MoodMatch → Response
```

Example: A productivity agent could delegate mood management to MoodMatch when detecting user stress.

---

## 📁 Project Structure

```
moodmatch-agent/
├── agents/
│   ├── __init__.py
│   └── moodmatch_agent.py          # Main A2A agent orchestrator
├── config/
│   ├── __init__.py
│   └── mood_mappings.py            # 52 mood system with media preferences
├── models/
│   ├── __init__.py
│   └── a2a.py                      # A2A protocol Pydantic models
├── services/
│   ├── __init__.py
│   ├── mood_analyzer.py            # Gemini-powered mood analysis
│   ├── music_service.py            # Spotify integration
│   ├── movie_service.py            # TMDB integration
│   └── book_service.py             # Google Books integration
├── examples/
│   ├── mood_analyzer_example.py    # Mood analysis examples
│   ├── music_service_example.py    # Music service examples
│   ├── movie_service_example.py    # Movie service examples
│   ├── book_service_example.py     # Book service examples
│   └── agent_example.py            # Complete agent examples
├── main.py                         # FastAPI server entry point
├── pyproject.toml                  # Project configuration
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 💬 Example Conversations

### Example 1: Stress Relief

**User**: "I've had a really tough day at work and I'm feeling completely drained."

**MoodMatch**: 
> I hear you—those exhausting days can really take it out of you. It sounds like you need something soothing to help you decompress and recharge.
>
> 🎵 **Music**: "Weightless" by Marconi Union  
> → Perfect match for stress relief. This scientifically-proven relaxing track will help lower your heart rate and ease tension. (8 min)  
> [Listen on Spotify](https://open.spotify.com/track/...)
>
> 🎬 **Movie**: The Secret Life of Walter Mitty (2013)  
> → Great choice for gentle escapism. This uplifting adventure will transport you away from daily stress with beautiful visuals and inspiring themes. (Drama, Adventure, Comedy) ⭐ 7.2/10  
> [Watch options](https://www.themoviedb.org/movie/...)
>
> 📚 **Book**: "The Midnight Library" by Matt Haig  
> → Excellent for perspective and hope. This thought-provoking novel explores life's possibilities and will help you find peace with where you are. (~6 hours) ⭐ 4.2/5  
> [Preview on Google Books](https://books.google.com/books?id=...)
>
> 💙 Take your time with any of these—you deserve to unwind.

### Example 2: Celebration

**User**: "Just got promoted! I want to celebrate!"

**MoodMatch**:
> That's amazing—congratulations on your promotion! 🎉 You've earned this moment, and it sounds like you're ready to really celebrate in style.
>
> 🎵 **Music**: "Happy" by Pharrell Williams  
> → Perfect celebration anthem! This upbeat, joyful track matches your triumphant energy and will keep your spirits soaring. (4 min)  
> [Listen on Spotify](https://open.spotify.com/track/...)
>
> 🎬 **Movie**: The Pursuit of Happyness (2006)  
> → Great choice for celebrating success. This inspiring true story of achievement and perseverance will resonate with your moment of triumph. (Biography, Drama) ⭐ 8.0/10  
> [Watch options](https://www.themoviedb.org/movie/...)
>
> 📚 **Book**: "Atomic Habits" by James Clear  
> → Excellent for sustaining momentum. This practical guide will help you build on this success and achieve even more. (~5 hours) ⭐ 4.4/5  
> [Preview on Google Books](https://books.google.com/books?id=...)
>
> 💙 Enjoy every moment of this achievement—you've worked hard for it!

---

## 💰 API Costs & Rate Limits

All APIs used by MoodMatch offer **generous free tiers**:

| Service | Free Tier | Rate Limit | Cost if Exceeded |
|---------|-----------|------------|------------------|
| **Gemini 2.0 Flash** | 1500 requests/day | 15 RPM | Free during experimental period |
| **Spotify** | Unlimited | No strict limit | Always free for basic API |
| **TMDB** | Unlimited | 30 requests/10s | Always free |
| **Google Books** | 1000 requests/day | - | $0.50 per 1000 requests after |

**Estimated costs for typical usage**: **$0/month** 🎉

*Based on ~100 user requests per day (well within all free tiers)*

---

## 🧪 Running Examples

The project includes comprehensive examples for all components:

```bash
# Test mood analysis
python examples/mood_analyzer_example.py

# Test music recommendations
python examples/music_service_example.py

# Test movie recommendations
python examples/movie_service_example.py

# Test book recommendations
python examples/book_service_example.py

# Test complete agent
python examples/agent_example.py
```

Each example demonstrates:
- Basic functionality
- Error handling
- Edge cases
- Best practices

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests** (once test suite is added)
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution

- 🧪 **Testing**: Unit and integration tests
- 📊 **Analytics**: Usage tracking and insights
- 🎨 **UI**: Web interface for the agent
- 🌍 **Internationalization**: Multi-language support
- 🔧 **Optimization**: Performance improvements
- 📚 **Documentation**: More examples and guides
- 🎵 **Features**: Additional media sources (podcasts, games, etc.)

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `Import "fastapi" could not be resolved`  
**Solution**: Install dependencies: `pip install -e .`

**Issue**: `Agent not initialized`  
**Solution**: Check your `.env` file has all required API keys

**Issue**: `Rate limit exceeded`  
**Solution**: Wait a few minutes or check API quotas

**Issue**: `No recommendations found`  
**Solution**: Agent will gracefully handle service failures. Check API keys are valid.

**Issue**: `CORS errors in browser`  
**Solution**: CORS is enabled for all origins in development. For production, configure `allow_origins` in `main.py`

---

## 📜 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2025 Olaitan34

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Google Gemini Team** - For the incredible Gemini 2.0 Flash model
- **Pydantic AI** - For making LLM integration elegant and type-safe
- **FastAPI** - For the amazing web framework
- **Spotify** - For comprehensive music data and APIs
- **TMDB** - For extensive movie database
- **Google Books** - For vast book catalog
- **A2A Protocol Contributors** - For the agent-to-agent standard
- **The Open Source Community** - For inspiration and support

---

## 📬 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Olaitan34/moodmatch-agent/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/Olaitan34/moodmatch-agent/discussions)
- **Email**: Create an issue for support

---

## 🌟 Star History

If you find MoodMatch useful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ using AI and modern Python**

[🏠 Home](https://github.com/Olaitan34/moodmatch-agent) • 
[📖 Docs](https://github.com/Olaitan34/moodmatch-agent/wiki) • 
[🐛 Issues](https://github.com/Olaitan34/moodmatch-agent/issues) • 
[💬 Discussions](https://github.com/Olaitan34/moodmatch-agent/discussions)

</div>
