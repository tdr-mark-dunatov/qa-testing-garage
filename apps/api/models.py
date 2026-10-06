"""
Database models for Webhook Pitstop
Racing-themed webhook inspection tool
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PitLaneRequest(Base):
    """
    Represents a webhook request entering the pit lane for inspection
    """
    __tablename__ = "pit_lane_requests"

    id = Column(Integer, primary_key=True, index=True)
    pit_id = Column(String(36), index=True, nullable=False, comment="Pit lane identifier (webhook ID)")
    method = Column(String(10), nullable=False, comment="HTTP method (engine type)")
    headers = Column(JSON, comment="Request headers (diagnostic data)")
    body = Column(Text, comment="Request body (payload)")
    query_params = Column(JSON, comment="Query parameters")
    ip_address = Column(String(45), comment="Source IP (starting grid position)")
    lap_time_ms = Column(Integer, comment="Response time in milliseconds")
    status_code = Column(Integer, default=200, comment="HTTP status code")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Timestamp (pit entry time)")
