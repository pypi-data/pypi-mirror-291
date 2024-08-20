from flask import Blueprint
from localstudio.app.utils.api import configure_api_from_blueprint

from localstudio.app.blueprints.entities.resources import (
    EntityPreviewFilesResource,
    EntityNewsResource,
    EntityTimeSpentsResource,
)


routes = [
    ("/data/entities/<entity_id>/news", EntityNewsResource),
    ("/data/entities/<entity_id>/preview-files", EntityPreviewFilesResource),
    ("/data/entities/<entity_id>/time-spents", EntityTimeSpentsResource),
]

blueprint = Blueprint("entities", "entities")
api = configure_api_from_blueprint(blueprint, routes)
