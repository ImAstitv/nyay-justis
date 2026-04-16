from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, cases, ocr, citizen
from seed_users import seed_users

app = FastAPI(title="JUSTIS API", version="2.0.0")

@app.on_event("startup")
def startup_event():
    seed_users()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nyay-justis.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])
app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
app.include_router(citizen.router, prefix="/citizen", tags=["citizen"])

@app.get("/")
def root():
    return {"status": "JUSTIS API running", "version": "2.0.0"}