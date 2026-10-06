"""
Database models for Webhook Pitstop
Racing-themed webhook inspection tool
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ReceivingBay(Base):
    """
    Represents a Webhook Receiving Bay (named or quick)
    """
    __tablename__ = "receiving_bays"

    id = Column(Integer, primary_key=True, index=True)
    bay_id = Column(String(100), unique=True, index=True, nullable=False, comment="Bay identifier (name or UUID)")
    bay_name = Column(String(200), comment="Human-readable bay name")
    description = Column(Text, comment="Bay description/purpose")
    is_named = Column(Integer, default=0, comment="1 if named bay, 0 if quick/random")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Bay creation time")
    last_request_at = Column(DateTime, comment="Last webhook received")

class PitLaneRequest(Base):
    """
    Represents a webhook request entering the receiving bay for inspection
    """
    __tablename__ = "pit_lane_requests"

    id = Column(Integer, primary_key=True, index=True)
    pit_id = Column(String(100), index=True, nullable=False, comment="Bay identifier (webhook ID)")
    method = Column(String(10), nullable=False, comment="HTTP method (engine type)")
    headers = Column(JSON, comment="Request headers (diagnostic data)")
    body = Column(Text, comment="Request body (payload)")
    query_params = Column(JSON, comment="Query parameters")
    ip_address = Column(String(45), comment="Source IP (starting grid position)")
    lap_time_ms = Column(Integer, comment="Response time in milliseconds")
    status_code = Column(Integer, default=200, comment="HTTP status code")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Timestamp (pit entry time)")
