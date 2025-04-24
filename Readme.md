# Email Intent Classifier

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

A machine learning application that classifies email intents using Streamlit.

📄 [View Report](https://drive.google.com/file/d/1b3kkjcUpzdoDfwNLDybKzrbcWz4hKQ0B/view?usp=sharing)

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
    ├── preprocessor.py   # Model Processor
    └── masker3.py        # Text processing module
```

## 🔧 Configuration

Ensure all model files are placed in the `models/` directory.

Modify `app.py` as needed to adjust:
- Categories
- UI elements
- Model paths

## 🌐 Access the App

After deployment, access it at:
[Email Classifier on Hugging Face](https://huggingface.co/spaces/VGreatVig07/Email_Classifier)

## 📝 License

MIT License - Feel free to modify and use.
