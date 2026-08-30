from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    gem_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    complaints = relationship("Complaint", back_populates="user")

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384)) # Using 384 for all-MiniLM-L6-v2
    verdict = Column(String) # TRUE, FALSE, MISLEADING, UNVERIFIABLE
    explanation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    evidences = relationship("Evidence", back_populates="claim")

class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    source_url = Column(String)
    chunk_text = Column(Text)
    similarity_score = Column(Float)

    claim = relationship("Claim", back_populates="evidences")

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    claim_id = Column(Integer, ForeignKey("claims.id"))
    source_url = Column(String, nullable=False)
    draft_text = Column(Text)
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="complaints")
    claim = relationship("Claim")
