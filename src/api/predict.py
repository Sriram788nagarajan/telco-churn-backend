from fastapi import APIRouter
from src.schemas.predict_schema import CustomerInput
from src.core.config import predict_single

router = APIRouter()

@router.post("/")
def predict_churn(customer: CustomerInput):
    input_dict = customer.dict()
    label, prob = predict_single(input_dict)
    return {
        "churn_probability": prob,
        "churn_label": label
    }
