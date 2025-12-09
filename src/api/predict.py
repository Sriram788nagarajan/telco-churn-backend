from fastapi import APIRouter
from schemas.predict_schema import CustomerInput
from core.config import predict_single

router = APIRouter()

@router.post("/")
def predict_churn(customer: CustomerInput):
    input_dict = customer.dict()
    label, prob = predict_single(input_dict)
    return {
        "churn_probability": prob,
        "churn_label": label
    }
