"""
Controllers for users
"""
import os
from functools import wraps

import jwt

from flask import request, jsonify
from models import User



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, os.getenv("APP_SECRET"), algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
