import os
from google import genai
import trafilatura
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, responses
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from schemas import NewsSearch, NewsArticle, NewsSummary, SummaryResults

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient()
    yield
    await app.state.client.aclose()
    
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get('/')
async def home():
    return responses.JSONResponse(content={'content': 'Welcome to Smart News Digest'})

@app.post("/general_news")
async def general_news(search: NewsSearch, request:Request):
    api_key = os.getenv('SERP_API_KEY')
    if not api_key:
        raise HTTPException(status_code=401, detail='Missing or Invalid SERPAPI Key')
    
    google_search = 'https://serpapi.com/search?'

    params= {
        'engine': 'google_news',
        'api_key': api_key,
        'gl':search.country,
        'hl':search.language,
        'q': search.keyword
    }

    client: httpx.AsyncClient = request.app.state.client
    response = await client.get(google_search, params=params)
    if response.status_code == 200:
        results = response.json()
        news_results = results['news_results']
        modified = news_results[:50] 
        return responses.JSONResponse(content={'modified': modified})
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f'Failed to fetch News:{response.text}'
        )

#From Chatgpt, Use headers 
@app.post('/news_trafilatura')
async def news_trafilatura(article: NewsArticle):
    try:
        # Get raw html content bypassing block bots using browser headers
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient() as client:
            response = await client.get(article.url, headers=headers, timeout=15.0)
            if response.status_code == 200:
                html = response.text
                extracted = trafilatura.extract(html, include_comments=False)
                return responses.JSONResponse(content={'content': extracted or article.title})
            else:
                return responses.JSONResponse(content={'content':article.title})
    except Exception as e:
        return responses.JSONResponse(content={'content':article.title})


@app.post('/get_article_summary', response_model=SummaryResults)
async def get_article_summary(summary:NewsSummary):
    if not summary.news_article or len(summary.news_article.strip()) < 50:
        return {'summary': summary.title}

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise HTTPException(status_code=401, detail='Missing Gemini Api Key')
    try:
        client = genai.Client(api_key=google_api_key)
        model = 'gemini-2.0-flash-lite'

        prompt = f"""
        Provide a concise and informative summary of the following news article.
        Focus on the main points, key events, and outcomes.
        The summary should be no longer than 3-5 sentences.

        Article:
        ---
        {summary.news_article}
        ---
        
        Concise Summary:
        """

        response = client.models.generate_content(model=model, contents=prompt)
        if response.candidates:
            parts = response.text
            if parts:
                return responses.JSONResponse(content={'summary': parts.strip()})
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Gemini generated no text content."
                )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Gemini did not provide a summary (no candidates). Prompt feedback: {response.prompt_feedback}"
            )

    except Exception as e:
        raise HTTPException(
                status_code=500,
                detail=f"An error occurred during summarization: {e}"
            )
 
'''
def create_file(country: str, keyword: str):
    extension = '.txt'
    country = country.title()
    file_name = f'{country}_{keyword}_news{extension}'
    counter = 1

    while os.path.exists(file_name):
        file_name = f'{country}_{keyword}_news_{counter}{extension}'
        counter += 1

    return file_name
'''
