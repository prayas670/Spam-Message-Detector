from flask import Flask, render_template, request, jsonify
from database import db, Prediction
import joblib
import os

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()

# Load model safely
if os.path.exists("spam_model.pkl") and os.path.exists("tfidf_vectorizer.pkl"):
    model = joblib.load("spam_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
else:
    print("⚠️ Model not found. Training new model...")
    from train import train_model
    model, vectorizer = train_model()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return render_template("index.html", error="Model not loaded properly.")

    message = request.form.get("message", "").strip()

    if not message:
        return render_template("index.html", error="Please enter a message.")

    vec = vectorizer.transform([message])
    pred = model.predict(vec)[0]

    # SAFE confidence calculation
    prob = max(model.predict_proba(vec)[0]) * 100

    result = "spam" if pred == 1 else "ham"

    # Save to DB
    new_entry = Prediction(
        message=message,
        result=result,
        confidence=prob
    )
    db.session.add(new_entry)
    db.session.commit()

    return render_template(
        "index.html",
        message=message,
        prediction_text=result,
        confidence=f"{prob:.1f}"
    )


@app.route('/history')
def history():
    try:
        data = Prediction.query.order_by(Prediction.id.desc()).limit(20).all()

        results = []
        for item in data:
            results.append({
                "message": item.message,
                "result": item.result,
                "confidence": item.confidence
            })

        return jsonify(results)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Failed to load history"}), 500


if __name__ == "__main__":
    app.run(debug=True)