# ─────────────────────────────────────────────
#  database.py  –  SQLAlchemy model
# ─────────────────────────────────────────────

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Prediction(db.Model):
    __tablename__ = "predictions"

    id         = db.Column(db.Integer, primary_key=True)
    message    = db.Column(db.Text, nullable=False)
    result     = db.Column(db.String(10), nullable=False)   # 'spam' or 'ham'
    confidence = db.Column(db.Float, nullable=False)        # probability %
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "message":    self.message,
            "result":     self.result,
            "confidence": round(self.confidence, 1),
            "timestamp":  self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
