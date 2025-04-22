import pickle

def load_model_tokenizer(model_path="models/email_classifier.pkl", tokenizer_path="models/tfidf_vectorizer.pkl"):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
    return model, tokenizer