# ─────────────────────────────────────────────
#  predict.py  –  Quick CLI prediction test
# ─────────────────────────────────────────────

import joblib

model      = joblib.load("spam_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

test_messages = [
    "Congratulations! You have won a free gift. Click now!",
    "Hey, are we still meeting tomorrow?",
    "URGENT: Your account has been compromised. Verify immediately.",
    "Please find the attached report.",
]

print("\n── Spam Detector Results ──")
for msg in test_messages:
    vec  = vectorizer.transform([msg])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0][pred]
    label = "SPAM 🚫" if pred == 1 else "HAM  ✅"
    print(f"{label}  ({prob*100:.1f}%)  →  {msg}")
