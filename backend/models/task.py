from datetime import datetime
from .db import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True)
    filename = db.Column(db.String(255))
    rtsp_url = db.Column(db.String(512))
    status = db.Column(db.String(20), default='queued')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    object_count = db.Column(db.Integer)
    processing_time = db.Column(db.Float)
    error = db.Column(db.Text)

    alerts = db.relationship('Alert', backref='task', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'rtsp_url': self.rtsp_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'object_count': self.object_count,
            'processing_time': self.processing_time,
            'error': self.error
        }