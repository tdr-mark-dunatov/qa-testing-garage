"""
Pydantic schemas for Webhook Pitstop
Racing-themed request/response models
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional

class PitLaneRequestSchema(BaseModel):
    """Schema for pit lane (webhook) requests"""
    id: int
    pit_id: str
    method: str
    headers: Dict[str, Any]
    body: Optional[str] = None
    query_params: Dict[str, Any]
    ip_address: str
    lap_time_ms: Optional[int] = None
    status_code: int = 200
    created_at: datetime

    class Config:
        from_attributes = True

class PitLaneCreateResponse(BaseModel):
    """Response when creating a new pit lane"""
    pit_id: str
    pit_lane_url: str
    message: str = "🏁 Pit lane ready for inspection!"

class DiagnosticSummary(BaseModel):
    """Summary statistics for a pit lane"""
    pit_id: str
    total_requests: int
    fastest_lap_ms: Optional[int] = None
    slowest_lap_ms: Optional[int] = None
    average_lap_ms: Optional[float] = None

class ReceivingBayCreate(BaseModel):
    """Request to create a named receiving bay"""
    bay_name: str
    description: Optional[str] = None

class ReceivingBaySchema(BaseModel):
    """Schema for receiving bay"""
    id: int
    bay_id: str
    bay_name: Optional[str] = None
    description: Optional[str] = None
    is_named: int
    created_at: datetime
    last_request_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReceivingBayWithStats(BaseModel):
    """Receiving bay with request statistics"""
    bay_id: str
    bay_name: Optional[str] = None
    description: Optional[str] = None
    is_named: bool
    created_at: datetime
    last_request_at: Optional[datetime] = None
    total_requests: int
    fastest_lap_ms: Optional[int] = None
