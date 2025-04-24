import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from pathlib import Path
from sklearn.exceptions import NotFittedError

class IntentClassifier:
    def __init__(self, model_paths):
        # Configure NLTK data path (Docker compatible)
        self._setup_nltk()
        
        # Verify and load models
        self._verify_model_paths(model_paths)
        self._load_models(model_paths)
        
        # Initialize preprocessing tools
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def _setup_nltk(self):
        """Configure NLTK data path and download required resources"""
        nltk_data_path = os.getenv('NLTK_DATA', '/usr/share/nltk_data')
        os.makedirs(nltk_data_path, exist_ok=True)
        nltk.data.path.append(nltk_data_path)
        
        try:
            # Verify resources are available
            stopwords.words('english')
            WordNetLemmatizer().lemmatize('test')
        except LookupError:
            # Download if not available
            nltk.download('stopwords', download_dir=nltk_data_path, quiet=True)
            nltk.download('wordnet', download_dir=nltk_data_path, quiet=True)
            nltk.download('omw-1.4', download_dir=nltk_data_path, quiet=True)

    def _verify_model_paths(self, model_paths):
        """Verify all model files exist"""
        for name, path in model_paths.items():
            if not Path(path).exists():
                raise FileNotFoundError(
                    f"Model file not found: {path} ({name}). "
                    f"Current working directory: {os.getcwd()}"
                )

    def _load_models(self, model_paths):
        """Safely load all required models with validation"""
        try:
            # Load TF-IDF vectorizer with validation
            self.tfidf = joblib.load(model_paths['tfidf'])
            if not hasattr(self.tfidf, 'vocabulary_'):
                raise NotFittedError("TF-IDF vectorizer is not fitted")
                
            # Load classifier model
            self.model = joblib.load(model_paths['model'])
            
            # Load label encoder
            self.le = joblib.load(model_paths['label_encoder'])
            
        except Exception as e:
            raise ValueError(f"Failed to load models: {str(e)}")

    def preprocess_text(self, text):
        """Standalone text cleaning function"""
        if not isinstance(text, str):
            return ""
            
        # Lowercase
        text = text.lower()
        
        # Remove email-specific patterns
        text = re.sub(r'\S+@\S+', ' ', text)  # Email addresses
        text = re.sub(r'http\S+', ' ', text)  # URLs
        text = re.sub(r'www\S+', ' ', text)   # URLs
        
        # Remove punctuation and numbers
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        
        # Tokenize and process
        tokens = text.split()
        tokens = [self.lemmatizer.lemmatize(token) 
                 for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def predict(self, text):
        """Make prediction on new text with error handling"""
        if not self.tfidf or not self.model or not self.le:
            raise RuntimeError("Classifier not properly initialized")
            
        try:
            # Preprocess
            cleaned_text = self.preprocess_text(text)
            
            # Vectorize
            vectorized = self.tfidf.transform([cleaned_text])
            
            # Predict
            prediction = self.model.predict(vectorized)
            
            # Return human-readable label
            return self.le.inverse_transform(prediction)[0]
            
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")


# Initialize with Docker-compatible paths
MODEL_DIR = Path(__file__).parent.parent / "models"
model_paths = {
    'tfidf': os.getenv('TFIDF_MODEL_PATH', str(MODEL_DIR / "tfidf_vectorizer_stack.pkl")),
    'model': os.getenv('CLASSIFIER_MODEL_PATH', str(MODEL_DIR / "intent_classifier_stack.pkl")),
    'label_encoder': os.getenv('LABEL_ENCODER_PATH', str(MODEL_DIR / "label_encoder_stack.pkl"))
}

# Initialize classifier with comprehensive error handling
try:
    classifier = IntentClassifier(model_paths)
    # Verify the TF-IDF vectorizer is properly fitted
    test_vector = classifier.tfidf.transform(["test email"])
    print("Classifier initialized successfully")
except Exception as e:
    print(f"Failed to initialize classifier: {str(e)}")
    classifier = None