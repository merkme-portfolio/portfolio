from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """
    Модель для хранения маппинга между оригинальными и короткими ссылками.

    Методы:
        from_dict(data): Обновляет поля объекта из словаря данных.
        save_to_db(): Добавляет объект в базу данных и сохраняет изменения.
    """

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(128), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def from_dict(cls, data):
        field_mapping = {
            'url': 'original',
            'custom_id': 'short',
        }
        instance = cls()
        for api_field, db_field in field_mapping.items():
            if api_field in data:
                setattr(instance, db_field, data[api_field])
        return instance

    @classmethod
    def is_exists(cls, short_id):
        return cls.query.filter_by(short=short_id).first() is not None
