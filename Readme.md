
# Email Intent Classifier

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)


A machine learning application that classifies email intents using Streamlit.
Report Link : ![Report](https://drive.google.com/file/d/12y5KKNWeJNSkWNvQ4bN-iw2l0iGojT6T/view?usp=sharing)

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

## 📂 Project Structure

```
.
├── app.py                # Streamlit application
├── requirements.txt      # Python dependencies
├── models/               # Pretrained models
│   ├── tfidf_vectorizer_stack.pkl
│   ├── intent_classifier_stack.pkl
│   └── label_encoder_stack.pkl
└── utils/
    └── preprocessor.py   # Model Processor
    └── masker3.py   # Text processing module
    
```

## 🔧 Configuration
### Place your model files in the models/ directory

### Update app.py if you need to modify:

```
- Categories
- UI elements
- Model paths

```

## 🌐 Access the App
### After running, open:
![App](https://huggingface.co/spaces/VGreatVig07/Email_Classifier)

## 📝 License
### MIT License - Feel free to modify and use
