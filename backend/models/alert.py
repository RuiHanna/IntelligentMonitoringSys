from .db import db


class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.String(36), primary_key=True)
    task_id = db.Column(db.String(36), db.ForeignKey('tasks.id'))
    alert_type = db.Column(db.String(50))
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    is_resolved = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'type': self.alert_type,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_resolved': self.is_resolved
        }