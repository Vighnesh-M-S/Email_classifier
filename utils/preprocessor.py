import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re

import os
os.environ['NLTK_DATA'] = '/app/nltk_data'

import nltk
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Tokenize
    words = text.split()

    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    # Lemmatization
    words = [lemmatizer.lemmatize(word) for word in words]

    return ' '.join(words)

def clean_and_vectorize(text, tokenizer):
    from .preprocessor import preprocess_text  # import your full preprocessing pipeline
    cleaned = preprocess_text(text)
    vectorized = tokenizer.transform([cleaned]).toarray()  # convert to dense
    return vectorized