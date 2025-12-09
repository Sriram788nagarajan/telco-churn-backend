from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.predict import router as predict_router

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount prediction endpoint
app.include_router(predict_router, prefix="/predict")

@app.get("/")
def root():
    return {"message": "Telco Churn Backend Running"}
