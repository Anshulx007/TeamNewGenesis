from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

app = FastAPI(
    title="SahajAI API",
    description="AI-powered government services assistant for Bharat",
    version="1.0.0",
)

# -----------------------
# Middleware
# -----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Register Routers
# -----------------------

app.include_router(chat.router)

# -----------------------
# Health & Root Endpoints
# -----------------------

@app.get("/")
def root():
    return {
        "service": "SahajAI Backend",
        "status": "running",
        "message": "Welcome to SahajAI API"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "SahajAI backend",
        "version": app.version
    }

# -----------------------
# Startup & Shutdown Events
# -----------------------

@app.on_event("startup")
def on_startup():
    print("🚀 SahajAI backend starting up...")

@app.on_event("shutdown")
def on_shutdown():
    print("🛑 SahajAI backend shutting down...")
