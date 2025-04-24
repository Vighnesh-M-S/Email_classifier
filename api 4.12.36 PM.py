from fastapi import APIRouter
from pydantic import BaseModel
from models.models import load_model_tokenizer
# from utils.preprocessor import preprocess_text
from utils.masker3 import mask_pii
from utils.preprocessor import IntentClassifier, model_paths  
import json


router = APIRouter()
classifier = IntentClassifier(model_paths)

model, tokenizer = load_model_tokenizer()

# nlp = spacy.load("en_core_web_sm") 

class EmailRequest(BaseModel):
    email: str

@router.post("/predict")
def predict(request: EmailRequest) -> dict:
    pii_result = mask_pii(request.email)
    masked_text = pii_result['masked_email']
    #print(json.dumps(pii_result, indent=2))
    #vector = clean_and_vectorize(pii_result["masked_email"], tokenizer)
    prediction = classifier.predict(masked_text)
   
    
    pii_result["category_of_the_email"] = prediction  # Optional override
    
    return pii_result
