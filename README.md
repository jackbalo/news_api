
# 📰 Smart News Digest API

Smart News Digest is a FastAPI-powered backend application that enables users to:
1. 🔍 Search for general news headlines using SerpAPI
2. 📄 Extract full article text from News urls using `trafilatura`
3. 🧠 Generate summaries of news articles using Google's Gemini API
 
---

## 🚀 Features

1. **Search News Headlines**
   a. Uses Google News Search engine and SERPAPI
   b. Parameters: country, language, keyword
   c. Returns up to 50 matching headline entries

2. **Extract Full Article Text**
   Uses `httpx` and `trafilatura` to fetch and parse readable article content from a given URL

3. **Summarize News Article**
   Integrates with Gemini (via `google.geneai`) to summarize articles in 3–5 sentences

---

## 🗂️ Project Structure

```
NEWS_API/
├── .env                  # Stores API keys (not committed to git)
├── main.py               # FastAPI application logic
├── requirements.txt      # Python dependencies
├── schemas.py            # Pydantic models for request/response validation
└── venv/                 # Python virtual environment
```

---

## ⚙️ Environment Variables

Create a `.env` file with the following content:

```env
SERP_API_KEY=your_serpapi_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the API

```bash
uvicorn main:app --reload
```

Access docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Endpoints Overview

### `GET /`
Returns a welcome message.

### `POST /general_news`
Searches for headlines.
- **Input**: `country`, `language`, `keyword`
- **Returns**: List of headlines

### `POST /news_trafilatura`
Extracts article body from a news URL.
- **Input**: `url`, `title`
- **Returns**: Full text content or fallback to title

### `POST /get_article_summary`
Summarizes a full article using Gemini.
- **Input**: `news_article`, `title`
- **Returns**: 3–5 sentence summary

---

## 🛠️ Tech Stack

- **FastAPI** – API framework
- **httpx** – Async HTTP client
- **Trafilatura** – HTML article text extractor
- **Gemini (Google)** – Content summarization
- **Pydantic** – Request/response validation
- **dotenv** – Environment variable loading

---

## 📌 Example Flow

1. User sends a POST to `/general_news` with a search term.
2. App fetches news headlines.
3. User selects a headline and sends the URL to `/news_trafilatura`.
4. The article content is extracted.
5. User can optionally send that content to `/get_article_summary` to receive a summary.

---

## 📄 License


---

## 🤝 Contributions
Author: blackBalo🖤

Feel free to fork, raise issues, or suggest improvements.
