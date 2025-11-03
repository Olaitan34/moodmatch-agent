# Telex.im Integration Guide

## 🚀 Quick Start

Your MoodMatch agent is now live and ready to integrate with Telex.im!

**Live URL:** `https://downier-virgulate-alanna.ngrok-free.dev`

---

## 📋 Integration Steps

### 1. Get Telex.im Access

Run this command in the HNG Slack #stage-3-backend channel:
```
/telex-invite your-email@example.com
```

### 2. Upload Workflow to Telex.im

Use the provided `telex_workflow.json` file in this repository.

**File location:** `./telex_workflow.json`

This workflow contains:
- Agent endpoint: `https://downier-virgulate-alanna.ngrok-free.dev/a2a/moodmatch`
- Full configuration for A2A protocol
- Mood categories and capabilities

### 3. Test on Telex.im

Once uploaded, chat with your agent:

**Example messages:**
- "I'm feeling stressed"
- "I'm so happy today!"
- "Feeling lonely"
- "I need something to cheer me up"
- "I'm broke and stressed" (it understands context!)

### 4. View Agent Logs

Check your agent's interactions:
```
https://api.telex.im/agent-logs/{channel-id}.txt
```

**How to get your channel-id:**
- Go to your Telex.im chat
- Copy the first UUID from the URL
- Example URL: `https://telex.im/telex-im/home/colleagues/01989dec-0d08-71ee-9017-00e4556e1942/...`
- Channel ID: `01989dec-0d08-71ee-9017-00e4556e1942`

---

## 🧪 Test the Integration

### Test 1: Health Check
```bash
curl https://downier-virgulate-alanna.ngrok-free.dev/health
```

**Expected:**
```json
{
  "status": "healthy",
  "agent": "MoodMatch A2A Agent",
  "version": "1.0.0",
  "agent_ready": true
}
```

### Test 2: Agent Endpoint (A2A Protocol)
```bash
curl -X POST https://downier-virgulate-alanna.ngrok-free.dev/a2a/moodmatch \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "execute",
    "params": {
      "messages": [
        {
          "role": "user",
          "parts": [
            {
              "kind": "text",
              "text": "I am happy"
            }
          ]
        }
      ]
    }
  }'
```

**Expected:** Full mood analysis + music/movie/book recommendations

---

## 📊 What the Agent Returns

When you send a mood to the agent, you'll get:

### 1. Mood Analysis
- Primary mood (one of 52 moods)
- Intensity level (1-10)
- Context understanding
- Secondary moods (if multi-mood)

### 2. Music Recommendation
- Track name and artist
- Spotify link
- Duration
- Why it matches your mood

### 3. Movie Recommendation
- Title, year, rating
- Genres
- Where to watch (Netflix, Prime, etc.)
- Why it matches your mood

### 4. Book Recommendation
- Title and author
- Reading time
- Links to Amazon, Goodreads, Google Books
- Why it matches your mood

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

## ⚠️ Important Notes

### Ngrok Limitations (Current Setup)
- ✅ **Great for testing:** Works perfectly for Telex.im integration testing
- ⚠️ **URL changes:** If you restart ngrok, you'll get a new URL
- ⚠️ **2-hour sessions:** Free plan has 2-hour limit (can restart)
- ⚠️ **Must be running:** Your computer needs to stay on

### For Production Deployment
Consider deploying to:
- **Railway.app** (free, auto-deploy from GitHub)
- **Render.com** (free tier available)
- **Fly.io** (free allowance)

These provide:
- ✅ Permanent URLs
- ✅ 24/7 uptime
- ✅ No session limits
- ✅ Better for final submission

---

## 🔧 Troubleshooting

### Issue: "Agent not responding on Telex.im"
**Check:**
1. Is your Python server running? (`python main.py`)
2. Is ngrok running? (`ngrok http 8000`)
3. Is the URL correct in `telex_workflow.json`?
4. Test the health endpoint in browser

### Issue: "Ngrok URL changed"
**Solution:**
1. Copy new ngrok URL
2. Update `telex_workflow.json`
3. Re-upload to Telex.im

### Issue: "Server stopped"
**Solution:**
```bash
# Restart Python server
python main.py

# Restart ngrok
ngrok http 8000
```

---

## 📝 Next Steps

1. ✅ Test agent on Telex.im chat
2. ✅ Try different moods
3. ✅ Check agent logs
4. ✅ Deploy to production (Railway/Render) for permanent URL
5. ✅ Write blog post about integration
6. ✅ Tweet about your agent
7. ✅ Submit to HNG

---

## 🎉 Success Checklist

Before submission, verify:
- [ ] Agent responds on Telex.im
- [ ] All 4 artifacts returned (mood + 3 recommendations)
- [ ] Clickable links work (Spotify, Netflix, Amazon)
- [ ] Agent logs show interactions
- [ ] Health endpoint accessible
- [ ] Documentation complete
- [ ] Blog post published
- [ ] Tweet posted with tags

---

**Questions?** Check the main [README.md](./README.md) or [POSTMAN_GUIDE.md](./POSTMAN_GUIDE.md)
