from flask .blueprints import Blueprint

auth=Blueprint('auth',__name__)

from  . import views
