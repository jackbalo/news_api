from pydantic import BaseModel, HttpUrl
from typing import Optional


class NewsSearch(BaseModel):
    country: Optional[str] = 'gh'
    keyword: str
    language: Optional[str] = 'en'


class NewsArticle(BaseModel):
    url: str
    title: str
    
    
class NewsSummary(BaseModel):
    news_article: str
    title:str
    
class SummaryResults(BaseModel):
    summary:str
        