from flask import Blueprint
from localstudio.app.utils.api import configure_api_from_blueprint

from localstudio.app.blueprints.events.resources import (
    EventsResource,
    LoginLogsResource,
)

routes = [
    ("/data/events/last", EventsResource),
    ("/data/events/login-logs/last", LoginLogsResource),
]

blueprint = Blueprint("events", "events")
api = configure_api_from_blueprint(blueprint, routes)
