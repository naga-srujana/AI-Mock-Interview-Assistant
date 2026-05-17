# 🎯 AI Mock Interview Assistant

A professional AI-powered mock interview assistant built with Python and Streamlit. This helps students practice interviews, analyze responses, and improve communication skills through intelligent real-time feedback.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Semantic Analysis | Compares your answer to an ideal response using sentence-transformers |
| 💬 Sentiment Detection | Detects positive/negative/neutral tone and emotional state |
| 🔤 Filler Word Detection | Identifies "um", "uh", "like", "basically", and more |
| ✅ Grammar Analysis | Checks grammar errors using LanguageTool |
| 📈 Confidence Score | Weighted score from grammar, fluency, sentiment, and relevance |
| 🤖 AI Feedback | Actionable suggestions to improve your answers |
| 📊 Visualizations | Gauge charts, bar charts, and score cards powered by Plotly |
| 📜 Session History | Tracks all past interview sessions |

---

## 🚀 Installation & Setup

### 1. Clone or Download the Project

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---


## 🔧 Tech Stack

- **Frontend:** Streamlit
- **NLP:** sentence-transformers, NLTK (VADER)
- **Grammar:** language-tool-python
- **Speech-to-Text:** SpeechRecognition + Google Web Speech API
- **Visualizations:** Plotly
- **Data:** pandas


---


## 📄 License

MIT License 
