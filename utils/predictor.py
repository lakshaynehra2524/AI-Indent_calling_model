import joblib


model = joblib.load("Model_Training/linear_svc_model.pkl")
vectorizer = joblib.load("Model_Training/tfidf_vectorizer.pkl")

def predict_intent(user_text):

    """
    Predicts user intent using
    trained Linear SVC model.
    """

    # Convert text to TF-IDF vector
    vector = vectorizer.transform([user_text])

    # Predict intent
    prediction = model.predict(vector)[0]

    return prediction
