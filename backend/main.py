from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, cases, ocr, citizen
from seed_users import seed_users

app = FastAPI(title="JUSTIS API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TEMPORARY (debug)
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
app.include_router(citizen.router, prefix="/citizen", tags=["citizen"])

@app.on_event("startup")
def startup_event():
    print("🔥 Seeding users...")
    seed_users()

@app.get("/")
def root():
    return {"status": "JUSTIS API running", "version": "2.0.0"}