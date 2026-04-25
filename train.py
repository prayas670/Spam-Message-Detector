# ─────────────────────────────────────────────
#  train.py  –  Train & save the spam model
# ─────────────────────────────────────────────

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load dataset
data = pd.read_csv("spam.csv")
data = data.rename(columns={'v1': 'label', 'v2': 'text'})
data = data[['label', 'text']]
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# 2. Split
X, y = data['text'], data['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Vectorise
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf  = vectorizer.transform(X_test)

# 4. Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# 5. Evaluate
y_pred = model.predict(X_test_tfidf)
print("Accuracy :", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 6. Save artefacts
joblib.dump(model,      "spam_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model and vectorizer saved!")
