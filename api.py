from fastapi import APIRouter
from pydantic import BaseModel
from models.models import load_model_tokenizer
from utils.preprocessor import clean_and_vectorize
from utils.masker3 import mask_pii
import json


router = APIRouter()

model, tokenizer = load_model_tokenizer()

# nlp = spacy.load("en_core_web_sm") 

class EmailRequest(BaseModel):
    email: str

@router.post("/predict")
def predict(request: EmailRequest) -> dict:
    pii_result = mask_pii(request.email)
    #print(json.dumps(pii_result, indent=2))
    vector = clean_and_vectorize(pii_result["masked_email"], tokenizer)
    prediction = model.predict(vector)[0]
    
    pii_result["category_of_the_email"] = prediction  # Optional override
    
    return pii_result
