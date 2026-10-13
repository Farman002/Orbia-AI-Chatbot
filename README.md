# 🤖 Orbia AI Chatbot

A locally running AI chatbot built with **Python, Streamlit, Ollama, and SQLite**. Nexa AI provides an interactive chat interface powered by the Llama 3.2 language model, with persistent conversation history stored locally.

## ✨ Features

- **AI-Powered Conversations:** Generate intelligent responses using Llama 3.2.
- **Local AI Inference:** Run the language model on your own computer using Ollama, without requiring paid cloud AI API credits.
- **Interactive Web Interface:** Chat through a clean, responsive Streamlit application.
- **Persistent Chat History:** Store conversations and messages in a local SQLite database.
- **Conversation Management:** Create new chats, reopen previous conversations, and delete conversations with confirmation.
- **Automatic Chat Titles:** Generate conversation titles from the first user message.
- **Message Timestamps:** Display timestamps for saved messages.
- **Conversation Context:** Include previous messages when generating follow-up responses.
- **Secure Configuration:** Keep credentials out of source control using environment files and `.gitignore`.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web-based chat interface |
| Ollama | Local AI model runtime |
| Llama 3.2 | Language model |
| SQLite | Persistent conversation storage |
| Git and GitHub | Version control |

## 📂 Project Structure

```text
AI_Chatbot/
│
├── app.py              # Streamlit user interface
├── chatbot.py          # Ollama integration and AI responses
├── database.py         # SQLite database operations
├── test_chatbot.py     # AI integration test
├── requirements.txt    # Python dependencies
├── .gitignore          # Excluded files and secrets
├── .env                # Optional local environment variables
├── chat_history.db     # Local conversation database
└── README.md           # Project documentation
```

> The `.env` file and `chat_history.db` are local files and should not be committed to GitHub.

## ⚙️ Prerequisites

Before running the application, install:

- Python 3.10 or newer
- Git
- Ollama for Windows, macOS, or Linux
- A computer with sufficient RAM to run the selected AI model

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Farman002/orbia-ai-chatbot.git
cd nexa-ai-chatbot
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, install the main packages manually:

```bash
python -m pip install streamlit ollama
```

### 4. Install Ollama

Download Ollama from:

https://ollama.com/download

Install it and verify the installation:

```bash
ollama --version
```

### 5. Download the Llama 3.2 model

```bash
ollama pull llama3.2
```

Verify that the model is available:

```bash
ollama list
```

You can test the model directly:

```bash
ollama run llama3.2
```

Enter a question and verify that the model responds. Type `/bye` to exit the interactive session.

### 6. Run the chatbot

From your project directory, execute:

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

http://localhost:8501

Open the URL in your browser to start chatting with Nexa AI.

## 💬 How to Use

1. Launch the application.
2. Click **Start a new chat** to create a conversation.
3. Enter a question in the message box.
4. Wait for Llama 3.2 to generate a response.
5. Use the sidebar to reopen previous conversations.
6. Click the trash icon beside a conversation to request deletion.
7. Confirm or cancel the deletion when prompted.

Conversations are stored in SQLite and remain available after restarting the application, provided the database file is preserved.

## 🗄️ Database Design

The application uses SQLite to store conversation data.

### Conversations table

Stores information about each chat:

- `id`: Unique conversation identifier
- `title`: Conversation title
- `created_at`: Conversation creation timestamp

### Messages table

Stores messages associated with each conversation:

- `id`: Unique message identifier
- `conversation_id`: Associated conversation
- `role`: `user` or `assistant`
- `content`: Message text
- `created_at`: Message timestamp

Each conversation can contain multiple messages. Deleting a conversation also deletes its associated messages when SQLite foreign-key enforcement is enabled.

## 🧪 Testing

Test the SQLite database:

```bash
python test_database.py
```

Test the Ollama integration:

```bash
python test_chatbot.py
```

The AI integration test requires Ollama to be installed and running, with the `llama3.2` model available.

## 🔒 Privacy and Security

- AI prompts are processed by the local Ollama model.
- Conversation history is stored in the local SQLite database.
- No OpenAI API key is required by the current Ollama-based implementation.
- Do not commit `.env`, virtual environments, or local database files.
- Avoid exposing the application to untrusted networks without adding appropriate authentication and security controls.

## ⚠️ Troubleshooting

**Ollama connection error**

Ensure Ollama is running and the local service is available.

```bash
ollama list
```

**Model not found**

Download the model again:

```bash
ollama pull llama3.2
```

**Streamlit module not found**

Install Streamlit in your active virtual environment:

```bash
python -m pip install streamlit
```

**Conversation history is missing**

Ensure you are using the same `chat_history.db` file and project directory as before.

**Application starts but responses are slow**

Local model performance depends on available RAM, CPU/GPU resources, and other applications running on your computer.

## 🔮 Future Improvements

- Search and filter conversations
- Group conversation history by date
- Add Markdown code highlighting and copy buttons
- Add model selection
- Add response streaming
- Export conversations to TXT or PDF
- Support document question answering using RAG
- Add unit tests and improved error handling
- Add optional authentication for multi-user access

## 👨‍💻 Author

**Farman Naim**

Computer Science | Python Development | AI Applications

GitHub: https://github.com/Farman002

LinkedIn: https://www.linkedin.com/in/farman-naim

## 📄 License

This project is available for educational and portfolio use. Add a license file if you want to specify formal permissions for reuse and distribution.
