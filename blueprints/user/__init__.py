"""
CRUD for endpoint user
"""

from flask import Blueprint

from controllers.user_control import token_required
from models import User
from flask import request, jsonify

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/user')
@token_required
def function():
    pass