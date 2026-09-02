import os
from google import genai
from datetime import datetime

def generate_verdict(claim: str, evidence_chunks: list[str]) -> dict:
    """
    Generates a verdict using Google Gemini based on the claim and retrieved evidence.
    Returns a dict with 'verdict' and 'explanation'.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "verdict": "UNVERIFIABLE",
            "explanation": "GEMINI_API_KEY environment variable is not set."
        }
        
    client = genai.Client(api_key=api_key)
    
    evidence_text = "\n\n---\n\n".join(evidence_chunks)
    current_date = datetime.now().strftime("%B %Y")
    
    prompt = f"""
    You are an expert fact-checker. The current date is {current_date}. Evaluate the following claim using ONLY the provided evidence.
    
    Claim: {claim}
    
    Evidence:
    {evidence_text}
    
    Based on the evidence, classify the claim into exactly one of these categories:
    TRUE, FALSE, MISLEADING, UNVERIFIABLE.
    
    Provide your response in exactly the following format:
    VERDICT: [Your classification]
    EXPLANATION: [A brief explanation of why, referencing the evidence]
    """
    
    max_retries = 3
    import time
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            text = response.text
            break
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"LLM Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return {
                    "verdict": "UNVERIFIABLE",
                    "explanation": f"Failed to generate verdict due to API error: {e}"
                }
        
        # Parse the response
    verdict = "UNVERIFIABLE"
    explanation = text
    
    for line in text.split('\n'):
        clean_line = line.replace("*", "").strip()
        if clean_line.startswith("VERDICT:"):
            verdict_str = clean_line.replace("VERDICT:", "").strip().upper()
            if "TRUE" in verdict_str: verdict = "TRUE"
            elif "FALSE" in verdict_str: verdict = "FALSE"
            elif "MISLEADING" in verdict_str: verdict = "MISLEADING"
        elif clean_line.startswith("EXPLANATION:"):
            explanation = clean_line.replace("EXPLANATION:", "").strip()
            break # the rest of the text is the explanation
            
    # Handle case where EXPLANATION might span multiple lines
    if "EXPLANATION:" in text:
        explanation = text.replace("*", "").split("EXPLANATION:")[1].strip()

        
    return {
        "verdict": verdict,
        "explanation": explanation
    }
