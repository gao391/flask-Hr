from flask import Blueprint, redirect, session, request, jsonify, render_template
from Models.models import Commodity

from exts import db

bp = Blueprint('qa', __name__, url_prefix="/")


@bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect('/')
    return redirect('/auth/login')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/auth/login')
