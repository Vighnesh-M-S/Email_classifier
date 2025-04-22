from fastapi import APIRouter
from pydantic import BaseModel
from models.models import load_model_tokenizer
from utils.preprocessor import clean_and_vectorize
from utils.pii_masker import mask_pii
# import spacy

router = APIRouter()

model, tokenizer = load_model_tokenizer()

# nlp = spacy.load("en_core_web_sm") 

class EmailRequest(BaseModel):
    email: str

@router.post("/predict")
def predict(request: EmailRequest):
    masked_email = mask_pii(request.email)
    vector = clean_and_vectorize(request.email, tokenizer)
    prediction = model.predict(vector)[0]  # model expects 2D array
    return {
        "prediction": prediction,
        "masked_email": masked_email
    }
