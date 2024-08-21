from lanstudio.app import db
from lanstudio.app.models.serializer import SerializerMixin
from lanstudio.app.models.base import BaseMixin


class Studio(db.Model, BaseMixin, SerializerMixin):
    """
    Describe a studio.
    """

    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False)
    archived = db.Column(db.Boolean(), default=False)
