from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import predict
from database import engine, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UniLoan AI API",
    description="Explainable Smart Loan Evaluation System Backend",
    version="1.0.0"
)

# CORS configuration for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modules
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def read_root():
    return {"message": "Welcome to UniLoan AI API. Go to /docs for Swagger UI documentation."}
