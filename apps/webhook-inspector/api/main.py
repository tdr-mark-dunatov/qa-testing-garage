"""
🏁 Webhook Pitstop - FastAPI Backend
Race-speed webhook inspection and diagnostics
"""
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid
import time
import os
import re
from typing import Dict, List

from database import engine, get_db
from models import Base, PitLaneRequest, ReceivingBay
from schemas import (
    PitLaneRequestSchema,
    PitLaneCreateResponse,
    DiagnosticSummary,
    ReceivingBayCreate,
    ReceivingBaySchema,
    ReceivingBayWithStats
)
from pii_detector import PIIDetector

# Initialize PII detector
pii_detector = PIIDetector()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🏁 Webhook Pitstop",
    description="Race-speed webhook inspection and diagnostics for QA testing",
    version="1.0.0"
)

# CORS for React frontend
# In production with Docker, nginx proxies requests so CORS isn't needed
# But we keep it flexible for development and non-Docker deployments
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://localhost,http://localhost:80"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.getenv("CORS_ALLOW_ALL") == "true" else ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════════
# WebSocket Connection Manager (Real-time Pit Lane Updates)
# ═══════════════════════════════════════════════════════════════════

class PitCrewManager:
    """Manages WebSocket connections for real-time pit lane updates"""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, pit_id: str, websocket: WebSocket):
        """Pit crew member joins the pit lane"""
        await websocket.accept()
        if pit_id not in self.active_connections:
            self.active_connections[pit_id] = []
        self.active_connections[pit_id].append(websocket)
        print(f"🏁 Pit crew connected to pit lane: {pit_id}")

    def disconnect(self, pit_id: str, websocket: WebSocket):
        """Pit crew member leaves the pit lane"""
        if pit_id in self.active_connections:
            self.active_connections[pit_id].remove(websocket)
            if not self.active_connections[pit_id]:
                del self.active_connections[pit_id]
            print(f"👋 Pit crew disconnected from pit lane: {pit_id}")

    async def broadcast(self, pit_id: str, message: dict):
        """Broadcast diagnostic data to all pit crew members"""
        if pit_id in self.active_connections:
            for connection in self.active_connections[pit_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass  # Connection might be closed

pit_crew = PitCrewManager()

# ═══════════════════════════════════════════════════════════════════
# Security: Data Masking for Sensitive Information
# ═══════════════════════════════════════════════════════════════════

def mask_sensitive_data(text: str) -> str:
    """
    Mask sensitive data in webhook payloads for security/compliance.

    Masks:
    - SSN: 123-45-6789 → ***-**-6789
    - Credit Cards: 1234-5678-9012-3456 → ****-****-****-3456
    - Email: john.doe@example.com → j***@example.com
    - Phone: (555) 123-4567 → (***) ***-4567
    """
    if not text:
        return text

    # Mask SSN (US format: 123-45-6789 or 123456789)
    text = re.sub(r'\b\d{3}-\d{2}-(\d{4})\b', r'***-**-\1', text)
    text = re.sub(r'\b(\d{3})(\d{2})(\d{4})\b', r'***\2\3', text)

    # Mask credit cards (various formats)
    text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?(\d{4})\b', r'****-****-****-\1', text)

    # Mask email addresses (keep domain for context)
    text = re.sub(r'\b([a-zA-Z])[a-zA-Z0-9._%+-]*@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', r'\1***@\2', text)

    # Mask phone numbers
    text = re.sub(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?(\d{4})\b', r'(***) ***-\1', text)

    return text

# ═══════════════════════════════════════════════════════════════════
# API Endpoints
# ═══════════════════════════════════════════════════════════════════

@app.get("/")
def read_root():
    """Welcome to the pit lane!"""
    return {
        "message": "🏁 Welcome to Webhook Pitstop!",
        "tagline": "Inspect webhooks at race speed",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "🏁 Ready to race!", "engine": "running"}

# ═══════════════════════════════════════════════════════════════════
# Receiving Bay Management
# ═══════════════════════════════════════════════════════════════════

@app.post("/api/bay/named", response_model=PitLaneCreateResponse)
def create_named_bay(bay_data: ReceivingBayCreate, request: Request, db: Session = Depends(get_db)):
    """
    🏁 Create a named Webhook Receiving Bay

    Named bays are reusable and easy to remember for repeated testing
    """
    import re
    import datetime

    # Sanitize bay name to URL-safe format
    bay_id = re.sub(r'[^a-z0-9-]', '-', bay_data.bay_name.lower()).strip('-')

    # Check if bay already exists
    existing = db.query(ReceivingBay).filter(ReceivingBay.bay_id == bay_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Receiving bay '{bay_id}' already exists!")

    # Create named bay
    bay = ReceivingBay(
        bay_id=bay_id,
        bay_name=bay_data.bay_name,
        description=bay_data.description,
        is_named=1,
        created_at=datetime.datetime.utcnow()
    )
    db.add(bay)
    db.commit()
    db.refresh(bay)

    base_url = str(request.base_url).rstrip('/')
    bay_url = f"{base_url}/bay/{bay_id}"

    return PitLaneCreateResponse(
        pit_id=bay_id,
        pit_lane_url=bay_url,
        message=f"🏁 Receiving Bay '{bay_data.bay_name}' ready!"
    )

@app.post("/api/bay/quick", response_model=PitLaneCreateResponse)
def create_quick_bay(request: Request, db: Session = Depends(get_db)):
    """
    ⚡ Create a quick (random) Webhook Receiving Bay

    Quick bays have random UUIDs for one-off testing
    """
    import datetime

    bay_id = str(uuid.uuid4())

    # Create quick bay
    bay = ReceivingBay(
        bay_id=bay_id,
        bay_name=f"Quick Bay {bay_id[:8]}",
        is_named=0,
        created_at=datetime.datetime.utcnow()
    )
    db.add(bay)
    db.commit()

    base_url = str(request.base_url).rstrip('/')
    bay_url = f"{base_url}/bay/{bay_id}"

    return PitLaneCreateResponse(
        pit_id=bay_id,
        pit_lane_url=bay_url,
        message=f"⚡ Quick bay {bay_id[:8]} ready!"
    )

@app.get("/api/bays", response_model=List[ReceivingBayWithStats])
def list_all_bays(db: Session = Depends(get_db)):
    """
    📋 List all Receiving Bays with statistics

    Returns all named and quick bays with request counts
    """
    from sqlalchemy import func

    bays = db.query(ReceivingBay).order_by(ReceivingBay.created_at.desc()).all()

    result = []
    for bay in bays:
        # Get stats for this bay
        stats = db.query(
            func.count(PitLaneRequest.id).label('total'),
            func.min(PitLaneRequest.lap_time_ms).label('fastest')
        ).filter(PitLaneRequest.pit_id == bay.bay_id).first()

        result.append(ReceivingBayWithStats(
            bay_id=bay.bay_id,
            bay_name=bay.bay_name,
            description=bay.description,
            is_named=bool(bay.is_named),
            created_at=bay.created_at,
            last_request_at=bay.last_request_at,
            total_requests=stats.total or 0,
            fastest_lap_ms=stats.fastest
        ))

    return result

@app.post("/api/pit/new", response_model=PitLaneCreateResponse)
def create_pit_lane(request: Request, db: Session = Depends(get_db)):
    """
    🏁 Create a new pit lane for webhook inspection (LEGACY - use /api/bay/quick instead)

    Generates a unique pit ID and webhook URL
    """
    # This now creates a quick bay for backward compatibility
    return create_quick_bay(request, db)

@app.api_route("/pit/{pit_id}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.api_route("/bay/{pit_id}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def inspect_webhook(
    pit_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    🔧 Main webhook inspection endpoint - captures ALL requests

    This is where the magic happens! Any HTTP request to this endpoint
    is captured, stored, and broadcast to connected pit crew members.

    Works with both /pit/{id} (legacy) and /bay/{id} (new)
    """
    import datetime
    start_time = time.time()

    # Capture request details
    body = await request.body()
    body_text = body.decode('utf-8', errors='replace') if body else None

    # 🚨 PII DETECTION - Scan for sensitive data
    pii_result = None
    if body_text:
        try:
            # Try to parse as JSON first
            import json
            try:
                body_json = json.loads(body_text)
                pii_result = pii_detector.detect(body_json)
            except json.JSONDecodeError:
                # Scan as plain text
                pii_result = pii_detector.detect(body_text)
        except Exception as e:
            print(f"⚠️ PII detection error: {e}")

    # Apply data masking for security compliance
    masked_body = mask_sensitive_data(body_text) if body_text else None

    # Create diagnostic record (with masked sensitive data)
    pit_request = PitLaneRequest(
        pit_id=pit_id,
        method=request.method,
        headers=dict(request.headers),
        body=masked_body,
        query_params=dict(request.query_params),
        ip_address=request.client.host if request.client else "unknown",
        lap_time_ms=0,  # Will be updated below
        status_code=200
    )

    db.add(pit_request)
    db.commit()
    db.refresh(pit_request)

    # Calculate lap time
    lap_time_ms = int((time.time() - start_time) * 1000)
    pit_request.lap_time_ms = lap_time_ms
    db.commit()

    # Update bay's last_request_at timestamp
    bay = db.query(ReceivingBay).filter(ReceivingBay.bay_id == pit_id).first()
    if bay:
        bay.last_request_at = datetime.datetime.utcnow()
        db.commit()

    # Broadcast to pit crew (WebSocket clients) with PII detection results
    await pit_crew.broadcast(pit_id, {
        "id": pit_request.id,
        "method": pit_request.method,
        "headers": pit_request.headers,
        "body": pit_request.body,
        "query_params": pit_request.query_params,
        "ip_address": pit_request.ip_address,
        "lap_time_ms": lap_time_ms,
        "pii_detected": pii_result.to_dict() if pii_result else None,
        "status_code": 200,
        "created_at": pit_request.created_at.isoformat(),
        "message": f"⚡ {pit_request.method} request captured in {lap_time_ms}ms"
    })

    return {
        "status": "ok",
        "message": f"🏁 Request inspected successfully",
        "lap_time_ms": lap_time_ms,
        "pit_id": pit_id
    }

@app.get("/api/pit/{pit_id}/requests", response_model=List[PitLaneRequestSchema])
def get_pit_lane_requests(pit_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """
    📋 Get inspection history for a pit lane

    Returns the most recent requests (default: 50)
    """
    requests = db.query(PitLaneRequest).filter(
        PitLaneRequest.pit_id == pit_id
    ).order_by(PitLaneRequest.created_at.desc()).limit(limit).all()

    return requests

@app.get("/api/pit/{pit_id}/diagnostics", response_model=DiagnosticSummary)
def get_pit_diagnostics(pit_id: str, db: Session = Depends(get_db)):
    """
    📊 Get diagnostic summary for a pit lane

    Returns statistics: total requests, fastest/slowest lap times, etc.
    """
    requests = db.query(PitLaneRequest).filter(PitLaneRequest.pit_id == pit_id).all()

    if not requests:
        raise HTTPException(status_code=404, detail=f"No diagnostics found for pit {pit_id}")

    lap_times = [r.lap_time_ms for r in requests if r.lap_time_ms is not None]

    return DiagnosticSummary(
        pit_id=pit_id,
        total_requests=len(requests),
        fastest_lap_ms=min(lap_times) if lap_times else None,
        slowest_lap_ms=max(lap_times) if lap_times else None,
        average_lap_ms=sum(lap_times) / len(lap_times) if lap_times else None
    )

@app.delete("/api/pit/{pit_id}/requests")
def clear_pit_lane(pit_id: str, db: Session = Depends(get_db)):
    """
    🗑️ Clear all requests from a pit lane

    Useful for cleaning up after testing
    """
    deleted_count = db.query(PitLaneRequest).filter(PitLaneRequest.pit_id == pit_id).delete()
    db.commit()

    return {
        "status": "cleared",
        "message": f"🧹 Cleared {deleted_count} requests from pit {pit_id[:8]}",
        "deleted_count": deleted_count
    }

@app.delete("/api/bay/{bay_id}")
def delete_bay(bay_id: str, db: Session = Depends(get_db)):
    """
    🗑️ Delete a receiving bay completely (COMPLIANCE FEATURE)

    Deletes the bay and all associated requests.
    Critical for data cleanup and compliance.
    """
    # Check if bay exists
    bay = db.query(ReceivingBay).filter(ReceivingBay.bay_id == bay_id).first()
    if not bay:
        raise HTTPException(status_code=404, detail=f"Bay '{bay_id}' not found")

    # Delete all requests for this bay
    requests_deleted = db.query(PitLaneRequest).filter(PitLaneRequest.pit_id == bay_id).delete()

    # Delete the bay itself
    db.delete(bay)
    db.commit()

    return {
        "status": "deleted",
        "message": f"🗑️ Bay '{bay.bay_name}' deleted completely",
        "bay_id": bay_id,
        "requests_deleted": requests_deleted
    }

@app.delete("/api/bays/cleanup")
def cleanup_old_bays(older_than_days: int = 7, db: Session = Depends(get_db)):
    """
    🧹 Bulk cleanup: Delete bays older than X days (COMPLIANCE FEATURE)

    Default: Deletes bays older than 7 days
    Query param: ?older_than_days=30
    """
    import datetime
    from sqlalchemy import and_

    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=older_than_days)

    # Find old bays
    old_bays = db.query(ReceivingBay).filter(
        ReceivingBay.created_at < cutoff_date
    ).all()

    if not old_bays:
        return {
            "status": "no_action",
            "message": f"No bays older than {older_than_days} days found",
            "deleted_count": 0
        }

    deleted_bays = []
    total_requests_deleted = 0

    for bay in old_bays:
        # Delete requests
        requests_deleted = db.query(PitLaneRequest).filter(
            PitLaneRequest.pit_id == bay.bay_id
        ).delete()
        total_requests_deleted += requests_deleted

        deleted_bays.append({
            "bay_id": bay.bay_id,
            "bay_name": bay.bay_name,
            "age_days": (datetime.datetime.utcnow() - bay.created_at).days,
            "requests_deleted": requests_deleted
        })

        # Delete bay
        db.delete(bay)

    db.commit()

    return {
        "status": "cleaned",
        "message": f"🧹 Deleted {len(deleted_bays)} bays older than {older_than_days} days",
        "deleted_count": len(deleted_bays),
        "total_requests_deleted": total_requests_deleted,
        "bays": deleted_bays
    }

@app.websocket("/ws/{pit_id}")
async def websocket_endpoint(websocket: WebSocket, pit_id: str):
    """
    🔄 WebSocket endpoint for real-time pit lane updates

    Pit crew members connect here to receive live updates
    """
    await pit_crew.connect(pit_id, websocket)
    try:
        while True:
            # Keep connection alive (client sends periodic pings)
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pit_crew.disconnect(pit_id, websocket)

# ═══════════════════════════════════════════════════════════════════
# Startup Event
# ═══════════════════════════════════════════════════════════════════

@app.on_event("startup")
def startup_event():
    """Print ASCII art on startup"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   🏁  WEBHOOK PITSTOP  🏁                                    ║
    ║                                                               ║
    ║   Inspect webhooks at race speed                             ║
    ║   FastAPI + WebSockets + Real-time Diagnostics               ║
    ║                                                               ║
    ║   Docs: http://localhost:8000/docs                           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
