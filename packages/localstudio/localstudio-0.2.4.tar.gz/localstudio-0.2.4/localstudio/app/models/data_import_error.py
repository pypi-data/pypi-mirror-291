from sqlalchemy.dialects.postgresql import JSONB

from localstudio.app import db
from localstudio.app.models.serializer import SerializerMixin
from localstudio.app.models.base import BaseMixin


class DataImportError(db.Model, BaseMixin, SerializerMixin):
    """
    Table to allow the storage of import errors.
    """

    event_data = db.Column(JSONB, nullable=False)
    source = db.Column(db.Enum("csv", "shotgun", name="import_source_enum"))
