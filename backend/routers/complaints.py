from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import trafilatura
from services.llm import genai
import os
import auth
import models

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

class VerifySourceRequest(BaseModel):
    claim: str
    url: str

class VerifySourceResponse(BaseModel):
    match: bool
    message: str
    draft: str = ""

@router.post("/verify-source", response_model=VerifySourceResponse)
def verify_source(request: VerifySourceRequest, current_user: models.User = Depends(auth.get_current_user)):
    url = request.url
    claim = request.claim
    
    # 1. Scrape the URL
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise Exception("Could not fetch the URL.")
        text = trafilatura.extract(downloaded)
        if not text:
            raise Exception("Could not extract text from the URL.")
    except Exception as e:
        return VerifySourceResponse(
            match=False, 
            message=f"Failed to scrape URL: {str(e)}"
        )
        
    # 2. Use LLM to verify if the scraped text contains/supports the claim
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")
        
    client = genai.Client(api_key=api_key)
    
    # Limit text to ~20000 chars to avoid token limits for this simple check
    text_snippet = text[:20000]
    
    prompt = f"""
    You are an expert fact-checker and content analyzer.
    Your task is to determine if the following article text makes, supports, or contains the specified claim.
    
    Claim being disputed: "{claim}"
    
    Article Text:
    {text_snippet}
    
    Does the article text contain or support the claim? Answer with EXACTLY "YES" or "NO".
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        answer = response.text.strip().upper()
        
        if "YES" in answer:
            # Generate a draft
            draft = f"Dear Editor/Publisher,\n\nI am writing to formally submit a complaint regarding the article published at {url}.\n\nAccording to an automated verification utilizing the AVeriTeC pipeline, the following claim made in your article has been rated as FALSE/MISLEADING:\n\"{claim}\"\n\nContinuing to host this content contributes to the spread of misinformation.\n\nPlease review the content and consider issuing a correction or removal.\n\nSincerely,\n{current_user.username}"
            return VerifySourceResponse(
                match=True,
                message="URL verified to contain the claim.",
                draft=draft
            )
        else:
            return VerifySourceResponse(
                match=False,
                message="The provided URL does not appear to contain the disputed claim."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM verification failed: {str(e)}")
