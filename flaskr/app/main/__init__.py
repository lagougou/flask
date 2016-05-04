from flask.blueprints import Blueprint
from ..models import Permission
from flask.ext.pagedown import PageDown

main=Blueprint('main',__name__)

from . import views,errors

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)