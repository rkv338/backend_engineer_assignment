import asyncio
import time
from typing import List, Optional
from datetime import datetime

import requests
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Search Engine API",
    description="A simple API endpoint for searching messages",
)

EXTERNAL_API_URL = "https://november7-730026606190.europe-west1.run.app/messages"

CACHE_TTL = 300
cache = {}
cache_timestamps = {}


class Message(BaseModel):
    id: Optional[int] = None
    content: Optional[str] = None
    timestamp: Optional[str] = None


class SearchResponse(BaseModel):
    results: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int


async def fetch_all_messages():
    
    cache_key = "all_messages"
    if cache_key in cache:
        cache_age = time.time() - cache_timestamps[cache_key]
        if cache_age < CACHE_TTL:
            return cache[cache_key]['items']
    
    
    try:
        
        response = await asyncio.to_thread(
            requests.get, 
            EXTERNAL_API_URL, 
            timeout=10.0,
            allow_redirects=True
        )
        response.raise_for_status()
        messages = response.json()
        
        cache[cache_key] = messages
        cache_timestamps[cache_key] = time.time()
        
        return messages['items']
    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch data from external API: {str(e)}"
        )


def search_messages(messages, query):

    if not query:
        return messages
    
    query_lower = query.lower()
    results = []
    
    for message in messages:
        if "message" in message:
            content = message["message"]
            if query_lower in content.lower():
                results.append(content)
        
    
    return results


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/search", response_model=SearchResponse)
async def search(q,page,page_size):
    start_time = time.time()
    
    try:
        all_messages = await fetch_all_messages()
        
        matching_messages = search_messages(all_messages, q)
        
        total = len(matching_messages)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        if page > total_pages and total_pages > 0:
            raise HTTPException(
                status_code=404,
                detail=f"Page {page} does not exist. Total pages: {total_pages}"
            )
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = matching_messages[start_idx:end_idx]
        
        response_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            results=paginated_results,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

