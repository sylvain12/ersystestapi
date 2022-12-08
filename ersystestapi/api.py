import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/clients', methods=('GET', 'POST'))
def client_list():
    if request.method == 'GET':
        return {"data": [], "message": "No data"}