from flask import Flask, render_template, request, jsonify
from database import db, Prediction
from classifier import classify_spam_category
import joblib
import os

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB & migration
with app.app_context():
    db.create_all()
    # Migration: Check if 'category' column exists in predictions table
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('predictions')]
    if 'category' not in columns:
        print("🚀 Migrating database: adding 'category' column...")
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE predictions ADD COLUMN category VARCHAR(50)"))
            conn.commit()
        print("✅ Migration completed successfully!")

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
    category = None
    if result == "spam":
        category = classify_spam_category(message)

    # Save to DB
    new_entry = Prediction(
        message=message,
        result=result,
        category=category,
        confidence=prob
    )
    db.session.add(new_entry)
    db.session.commit()

    return render_template(
        "index.html",
        message=message,
        prediction_text=result,
        category=category,
        confidence=f"{prob:.1f}"
    )


@app.route('/history')
def history():
    try:
        data = Prediction.query.order_by(Prediction.id.desc()).limit(20).all()
        return jsonify([item.to_dict() for item in data])
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Failed to load history"}), 500


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/api/stats')
def api_stats():
    try:
        total = Prediction.query.count()
        spam = Prediction.query.filter_by(result='spam').count()
        ham = Prediction.query.filter_by(result='ham').count()
        
        categories = ['Promotional', 'Scam', 'Fraud', 'Malware Links']
        category_counts = {}
        for cat in categories:
            category_counts[cat] = Prediction.query.filter_by(result='spam', category=cat).count()
            
        return jsonify({
            "total": total,
            "spam": spam,
            "ham": ham,
            "spam_rate": round((spam / total * 100), 1) if total > 0 else 0.0,
            "categories": category_counts
        })
    except Exception as e:
        print("STATS ERROR:", e)
        return jsonify({"error": "Failed to load stats"}), 500


@app.route('/api/history')
def api_history():
    try:
        records = Prediction.query.order_by(Prediction.id.desc()).all()
        return jsonify([r.to_dict() for r in records])
    except Exception as e:
        print("HISTORY API ERROR:", e)
        return jsonify({"error": "Failed to load history list"}), 500


@app.route('/api/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    try:
        record = Prediction.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return jsonify({"status": "success", "message": "Record deleted"})
        return jsonify({"status": "error", "message": "Record not found"}), 404
    except Exception as e:
        db.session.rollback()
        print("DELETE ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/clear_all', methods=['POST'])
def clear_all():
    try:
        db.session.query(Prediction).delete()
        db.session.commit()
        return jsonify({"status": "success", "message": "All history cleared"})
    except Exception as e:
        db.session.rollback()
        print("CLEAR ALL ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)