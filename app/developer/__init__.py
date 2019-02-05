from flask import Blueprint

bp = Blueprint('dev', __name__)

from app.developer import routes, src, models