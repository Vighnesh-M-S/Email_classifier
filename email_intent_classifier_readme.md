
# Email Intent Classifier

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A machine learning application that classifies email intents using Streamlit and Docker.

## 🚀 Quick Deployment

### Docker Installation
```bash
docker build -t email-classifier .
docker run -p 8501:8501 email-classifier
```

### Local Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

📂 Project Structure
.
├── app.py                # Streamlit application
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── models/               # Pretrained models
│   ├── tfidf_vectorizer_stack.pkl
│   ├── intent_classifier_stack.pkl
│   └── label_encoder_stack.pkl
└── utils/
    └── preprocessor.py   # Text processing module

🔧 Configuration
Place your model files in the models/ directory

Update app.py if you need to modify:

- Categories
- UI elements
- Model paths

🌐 Access the App
After running, open:
http://localhost:8501

📝 License
MIT License - Feel free to modify and use
