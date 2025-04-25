# Email Intent Classifier

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

A machine learning application that classifies email intents using Streamlit.

📄 [View Report](https://drive.google.com/file/d/1b3kkjcUpzdoDfwNLDybKzrbcWz4hKQ0B/view?usp=sharing)

## 📂 Project Structure

```
.
├── app.py                # Streamlit application
├── requirements.txt      # Python dependencies
├── models/               # Pretrained models
│   ├── tfidf_vectorizer_stack.pkl
│   ├── intent_classifier_stack.pkl
│   └── label_encoder_stack.pkl
|   └── nltk_data
|
└── utils/
    ├── preprocessor.py   # Model Processor
    └── masker3.py        # Text processing module
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Vighnesh-M-S/Email_classifier.git
cd Email_classifier
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

## 🧪 Example Query

Try inputting:

> "Subject: Data Analytics for Investment

I am contacting you to request information on data analytics tools that can be utilized with the Eclipse IDE for enhancing investment optimization. I am seeking suggestions for tools that can aid in making data-driven decisions. Particularly, I am interested in tools that can manage large datasets and offer advanced analytics features. These tools should be compatible with the Eclipse IDE and can smoothly integrate into my workflow You can reach me at liuwei@business.cn.. Key features I am interested in include data visualization, predictive modeling, and machine learning capabilities. I would greatly appreciate any recommendations or advice on how to begin with data analytics for investment optimization using the Eclipse IDE. My name is Elena Ivanova."

The system will return -
                {
"input_email_body":"Subject: Data Analytics for Investment

I am contacting you to request information on data analytics tools that can be utilized with the Eclipse IDE for enhancing investment optimization. I am seeking suggestions for tools that can aid in making data-driven decisions. Particularly, I am interested in tools that can manage large datasets and offer advanced analytics features. These tools should be compatible with the Eclipse IDE and can smoothly integrate into my workflow You can reach me at liuwei@business.cn.. Key features I am interested in include data visualization, predictive modeling, and machine learning capabilities. I would greatly appreciate any recommendations or advice on how to begin with data analytics for investment optimization using the Eclipse IDE. My name is Elena Ivanova."
"list_of_masked_entities":[
            0:{
                "position":[
                0:496
                1:514
                ]
                "classification":"email"
                "entity":"liuwei@business.cn"
                }
                1:{
                "position":[
                0:777
                1:790
                ]
                "classification":"full_name"
                "entity":"Elena Ivanova"
                }
                ]
                "masked_email":"Subject: Data Analytics for Investment
                
I am contacting you to request information on data analytics tools that can be utilized with the Eclipse IDE for enhancing investment optimization. I am seeking                            suggestions for tools that can aid in making data-driven decisions. Particularly, I am interested in tools that can manage large datasets and offer advanced analytics features. These tools should be compatible with the Eclipse IDE and can smoothly integrate into my workflow You can reach me at [email].. Key features I am interested in include data visualization, predictive modeling, and machine learning capabilities. I would greatly appreciate any recommendations or advice on how to begin with data analytics for investment optimization using the Eclipse IDE. My name is [full_name]."
                "category_of_the_email":"Request"
                }



## 🔧 Configuration

Ensure all model files are placed in the `models/` directory.

Modify `app.py` as needed to adjust:
- Categories
- UI elements
- Model paths

---

## 🛠 Tech Stack

🐍 Python 3.8+ – Core programming language

🎈 Streamlit – UI for interactive email classification

🐳 Docker – Containerization for easy deployment

📬 scikit-learn – ML models (SVM, Naive Bayes, Random Forest, Stacking)

🔤 TF-IDF Vectorizer – Feature extraction from text

🌍 langdetect – Language detection for multilingual support

🌐 Google Translate / Helsinki-NLP – Machine translation for non-English emails

🧼 Custom Preprocessor – Text cleaning and preprocessing

🧠 LabelEncoder – Encoding intent labels for classification

📊 Pandas, NumPy – Data manipulation and numerical operations
---



## 🌐 Access the App

After deployment, access it at:
[Email Classifier on Hugging Face](https://huggingface.co/spaces/VGreatVig07/Email_Classifier)

---

## 📄 License

MIT License © 2025

---
