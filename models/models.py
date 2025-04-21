import joblib
from sklearn.ensemble import RandomForestClassifier

def train_model(X_train, y_train):
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    joblib.dump(model, 'models/model.pkl')
    return model

def load_model(path='models/model.pkl'):
    return joblib.load(path)