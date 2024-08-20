from localstudio.app import db
from localstudio.app.models.serializer import SerializerMixin
from localstudio.app.models.base import BaseMixin


class FileStatus(db.Model, BaseMixin, SerializerMixin):
    """
    Describe the state of a given file.
    """

    name = db.Column(db.String(40), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False)
