# 💬 Gemini Chatbot — Flask

A plug-and-play chatbot using **Google Gemini API** + **Flask** backend.

---

## 🗂 File Structure

```
chatbot/
├── app.py                ← Flask backend + Gemini API logic
├── templates/
│   └── index.html        ← Chat UI (dark theme, responsive)
├── requirements.txt
├── .env.example          ← Copy to .env and add your keys
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API key**
3. Copy it

### 3. Configure your key

**Option A — .env file (recommended)**
```bash
cp .env.example .env
# Edit .env and paste your key
```

Then add this to the top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

**Option B — Environment variable**
```bash
# macOS/Linux
export GEMINI_API_KEY=your_key_here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_key_here"
```

**Option C — Directly in app.py** (quick test only, not for production)
```python
GEMINI_API_KEY = "your_key_here"
```

### 4. Run
```bash
python app.py
```
Open http://localhost:5000 in your browser.

---

## 🔌 Integrating into an Existing Project

If you already have a Flask app, just merge these parts:

**1. Add to your existing `app.py`:**
```python
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
chat_sessions = {}

@app.route("/api/chat", methods=["POST"])
def chat():
    # ... (copy the route from chatbot/app.py)
```

**2. Add the HTML** — copy `templates/index.html` into your templates folder,
or embed the `<style>` + chat markup into an existing page.

**3. If you use a URL prefix** (e.g. `/chatbot/api/chat`), update this line in `index.html`:
```js
const res = await fetch('/api/chat', { ... })
// change to:
const res = await fetch('/chatbot/api/chat', { ... })
```

---

## 🧠 Changing the Model

In `app.py`, change the `model_name`:

| Model | Speed | Intelligence |
|---|---|---|
| `gemini-1.5-flash` | Fast ⚡ | Good |
| `gemini-1.5-pro`   | Slower | Best |
| `gemini-1.0-pro`   | Medium | Older |

---

## 🛠 Customising the System Prompt

In `app.py`, edit `system_instruction`:
```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a study assistant for university students. ..."
)
```

---

## 🔒 Notes

- Chat history is kept **in-memory** per session. Restart the server = history cleared.
- For persistent history, store `chat_sessions` in a database (SQLite, Redis, etc.).
- Never expose your API key in frontend JS or commit `.env` to git.
