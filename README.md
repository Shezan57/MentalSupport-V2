# 🧠 MentalSupport-V2

An AI-powered mental health support system that provides empathetic therapeutic conversations, emergency assistance, and therapist location services. Built with LangChain, LangGraph, Groq AI, and integrated with Twilio for WhatsApp support.

## ✨ Features

- **🤖 AI Therapeutic Conversations**: Powered by MedGemma model via Ollama for professional mental health guidance
- **🚨 Emergency Support**: Automatic emergency call triggering via Twilio when crisis situations are detected
- **📍 Therapist Locator**: Find nearby licensed therapists using Google Maps API
- **💬 Multi-Channel Support**: 
  - Web interface via Streamlit
  - WhatsApp integration via Twilio
- **🔄 Intelligent Agent System**: Built with LangGraph for context-aware tool selection

## 🏗️ Architecture

```
MentalSupport-V2/
├── backend/
│   ├── main.py          # FastAPI server with /ask and /whatsapp_ask endpoints
│   ├── ai_agent.py      # LangGraph agent with tool definitions
│   ├── tools.py         # MedGemma and Twilio integration
│   └── config.py        # API keys and configuration
├── frontend.py          # Streamlit web interface
├── pyproject.toml       # Project dependencies
└── README.md
```

## 🛠️ Technologies

- **AI/ML**: LangChain, LangGraph, Groq (Llama 3.3), Ollama (MedGemma)
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Integrations**: Twilio (WhatsApp/Voice), Google Maps API
- **Package Manager**: UV (fast Python package installer)

## 📋 Prerequisites

- Python 3.13+
- [UV package manager](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.ai/) (for MedGemma model)
- API Keys:
  - Groq API key
  - Twilio account (SID, Auth Token, Phone Number)
  - Google Maps API key (for therapist location feature)

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Shezan57/MentalSupport-V2.git
cd MentalSupport-V2
```

2. **Install dependencies using UV**:
```bash
uv sync
```

3. **Install Ollama and pull MedGemma model**:
```bash
# Install Ollama from https://ollama.ai/
# Then pull the MedGemma model:
ollama pull alibayram/medgemma:4b
```

4. **Configure API keys**:
Edit `backend/config.py` with your credentials:
```python
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_FROM_NUMBER = "your_twilio_phone_number"
EMERGENCY_CONTACT = "emergency_contact_number"
GROQ_API_KEY = "your_groq_api_key"
GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
```

## 🎯 Usage

### Running the Backend

1. **Start Ollama** (in a separate terminal):
```bash
ollama serve
```

2. **Start the FastAPI backend**:
```bash
uv run backend/main.py
```

The backend will be available at `http://localhost:8000`

### Running the Frontend

In a new terminal:
```bash
uv run streamlit run frontend.py
```

The web interface will open at `http://localhost:8501`

### WhatsApp Integration

1. Configure Twilio WhatsApp sandbox or production number
2. Set webhook URL to: `https://your-domain.com/whatsapp_ask`
3. Use ngrok for local testing:
```bash
ngrok http 8000
```

## 🔧 API Endpoints

### POST `/ask`
Web interface endpoint for chat interactions.

**Request**:
```json
{
  "message": "I'm feeling anxious today"
}
```

**Response**:
```json
{
  "response": "I can sense how difficult anxiety can be...",
  "tool_called": "ask_mental_health_specialist"
}
```

### POST `/whatsapp_ask`
Twilio webhook endpoint for WhatsApp messages.

**Form Data**: `Body` (the user's message)

**Response**: TwiML XML format

## 🧰 Available Tools

The AI agent has access to three specialized tools:

1. **`ask_mental_health_specialist`**: Queries MedGemma for therapeutic responses
2. **`find_nearby_therapists_by_location`**: Searches for therapists using Google Maps
3. **`emergency_call_tool`**: Triggers emergency call via Twilio for crisis situations

## 🔒 Security Notes

- **NEVER commit `config.py`** with real API keys to version control
- Add `backend/config.py` to `.gitignore`
- Use environment variables for production deployments
- Implement proper authentication for production use

## 🐛 Troubleshooting

**Import Error: `cannot import name 'tool'`**
- Solution: Upgrade to LangChain v0.1.0+, import from `langchain_core.tools`

**Recursion Limit Error**
- Solution: Increase `recursion_limit` in config (already set to 50)

**JSONDecodeError in frontend**
- Solution: Ensure backend is running and accessible
- Check error handling in frontend (already implemented)

**Ollama Connection Error**
- Solution: Make sure Ollama is running (`ollama serve`)
- Verify MedGemma model is installed (`ollama list`)

## 📝 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## ⚠️ Disclaimer

This application is designed to provide supportive conversations and information about mental health. It is NOT a replacement for professional medical advice, diagnosis, or treatment. If you are experiencing a mental health emergency, please contact your local emergency services immediately.

---

**Built with ❤️ for mental health support**
