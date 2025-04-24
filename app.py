import streamlit as st
from utils.masker3 import mask_pii
from utils.preprocessor import IntentClassifier, model_paths


# Load classifier once
@st.cache_resource
def load_classifier():
    return IntentClassifier(model_paths)

classifier = load_classifier()

st.title("Email Classifier with PII Masking")

# Input email
email_input = st.text_area("Paste your email here:")

if st.button("Analyze"):
    if email_input.strip() == "":
        st.warning("Please enter an email.")
    else:
        # Step 1: Mask PII
        pii_result = mask_pii(email_input)

        # Step 2: Predict category
        masked_text = pii_result["masked_email"]
        prediction = classifier.predict(masked_text)
        pii_result["category_of_the_email"] = prediction
        # Step 3: Format full output
        # output = {
        #     "input_email_body": email_input,
        #     "list_of_masked_entities": sorted(result["entities"], key=lambda x: x["position"][0]),
        #     "masked_email": masked_text,
        #     "category_of_the_email": category
        # }

        # Step 4: Show output
        st.subheader("🔍 Analysis Result")
        st.json(pii_result)
