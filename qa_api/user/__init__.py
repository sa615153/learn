from flask import Blueprint, render_template, jsonify

mod = Blueprint('user', __name__, url_prefix='/user')