import json
from fastapi import APIRouter, Depends, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth
from services.embedding import get_bi_encoder
from pipeline import run_verification_pipeline_sse

router = APIRouter(prefix="/api/claims", tags=["claims"])

@router.post("/verify/stream")
async def verify_claim_stream(
    request: Request,
    claim: schemas.ClaimRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    SSE endpoint for verifying a claim.
    1. Checks Fast Path (pgvector).
    2. If miss, streams the Slow Path pipeline progress.
    """
    # Fast path check
    bi_encoder = get_bi_encoder()
    embedding_tensor = bi_encoder.encode(claim.content, convert_to_tensor=True)
    embedding_list = embedding_tensor.cpu().numpy().tolist()
    
    # Query pgvector for the closest claim
    similar_record = db.query(
        models.Claim,
        models.Claim.embedding.cosine_distance(embedding_list).label("distance")
    ).order_by("distance").first()
    
    async def event_generator():
        # Fast path check
        if similar_record and similar_record.distance < 0.05:
            cached_claim = similar_record.Claim
            yield {"data": json.dumps({"status": "processing", "message": "Fast Path: Found extremely similar verified claim in database!"})}
            
            result = {
                "verdict": cached_claim.verdict,
                "explanation": cached_claim.explanation,
                "evidence": [],
                "urls": ["Cached from Database"],
                "status": "complete"
            }
            yield {"data": json.dumps(result)}
            return
            
        # Slow Path
        async for progress_json in run_verification_pipeline_sse(claim.content):
            if await request.is_disconnected():
                break
                
            data = json.loads(progress_json)
            yield {"data": progress_json}
            
            # If complete, save to DB and award GEM
            if data.get("status") == "complete":
                new_claim = models.Claim(
                    content=claim.content,
                    embedding=embedding_list,
                    verdict=data.get("verdict"),
                    explanation=data.get("explanation")
                )
                db.add(new_claim)
                
                # Award GEM
                current_user.gem_score += 1
                
                db.commit()
                db.refresh(new_claim)
                
                # We could also save evidences to models.Evidence here
                
    return EventSourceResponse(event_generator())
