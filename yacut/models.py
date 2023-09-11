from datetime import datetime

from yacut import db

from .utils import Constants


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False, unique=True)
    short = db.Column(db.String(Constants.MAX_URL_LENGHT))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def to_dict(self):
        return dict(url=self.original)
