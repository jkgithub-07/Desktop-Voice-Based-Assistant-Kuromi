# 💀 Kuromi Desktop Assistant

An interactive, voice-based desktop assistant with ✨ chaotic energy ✨ inspired by Kuromi from Sanrio! This assistant listens, chats using LLMs, opens apps, gives you news, sends emails, and more — all with sass, music, and facial recognition.

---

## 🧠 Features
- 🎤 Voice-controlled assistant
- 🔐 Facial recognition authentication
- 🤖 LLM-powered responses via Groq (LLaMA 3)
- 🎧 Background music and animated GUI (Tkinter + GIFs)
- 🛜 Internet features: IP check, news, Wikipedia, YouTube, Google
- 📧 Gmail email sender with custom prompts
- 📚 Personality: Kuromi — bratty, cute, and chaotic

---

## 📁 Project Structure
```
assistant_git/
├── main.py                # Assistant logic
├── gui.py                 # GUI launcher
├── main2.py               # Facial recognition
├── online.py              # News, IP, email, web search
├── const.py               # Randomized Kuromi responses
├── gifs/                  # All animation gifs
├── music/                 # Background music {currently not in this repo
├── requirements.txt       # All dependencies
└── README.md              # You're here!
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/jkgithub-07/Desktop-Voice-Based-Assistant-Kuromi.git
cd Desktop-Voice-Based-Assistant-Kuromi
```

### 2. Create a `.env` File

`.env`:
```env
GROQ_API_KEY=your-groq-api-key
WOLFRAM_API_KEY=your-wolframalpha-key
EMAIL=your-gmail@gmail.com
EMAIL_PASSWORD=your-app-password
IP_API=your-ip-api-key
NEWS_API=your-news-api-key
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

---

## 🚀 Run the Assistant
```
python gui2.py
```
This will:
- Show a welcome animation 🎬
- Authenticate via webcam 🧠
- Start voice-based Kuromi mode 😈🎤

---

---

## 💖 Credits
- Inspired by Kuromi (Sanrio)
- LLM responses powered by [Groq](https://console.groq.com/)
- News from [NewsAPI.org](https://newsapi.org)
- Developed with chaotic vibes by [Janhvi Kurkure]

---

## 📜 License
MIT License © 2025
