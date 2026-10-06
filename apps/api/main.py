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
from typing import Dict, List

from database import engine, get_db
from models import Base, PitLaneRequest
from schemas import PitLaneRequestSchema, PitLaneCreateResponse, DiagnosticSummary

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

@app.post("/api/pit/new", response_model=PitLaneCreateResponse)
def create_pit_lane(request: Request):
    """
    🏁 Create a new pit lane for webhook inspection

    Generates a unique pit ID and webhook URL
    """
    pit_id = str(uuid.uuid4())
    base_url = str(request.base_url).rstrip('/')
    pit_lane_url = f"{base_url}/pit/{pit_id}"

    return PitLaneCreateResponse(
        pit_id=pit_id,
        pit_lane_url=pit_lane_url,
        message=f"🏁 Pit lane {pit_id[:8]} ready for inspection!"
    )

@app.api_route("/pit/{pit_id}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def inspect_webhook(
    pit_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    🔧 Main webhook inspection endpoint - captures ALL requests

    This is where the magic happens! Any HTTP request to this endpoint
    is captured, stored, and broadcast to connected pit crew members.
    """
    start_time = time.time()

    # Capture request details
    body = await request.body()
    body_text = body.decode('utf-8', errors='replace') if body else None

    # Create diagnostic record
    pit_request = PitLaneRequest(
        pit_id=pit_id,
        method=request.method,
        headers=dict(request.headers),
        body=body_text,
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

    # Broadcast to pit crew (WebSocket clients)
    await pit_crew.broadcast(pit_id, {
        "id": pit_request.id,
        "method": pit_request.method,
        "headers": pit_request.headers,
        "body": pit_request.body,
        "query_params": pit_request.query_params,
        "ip_address": pit_request.ip_address,
        "lap_time_ms": lap_time_ms,
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
