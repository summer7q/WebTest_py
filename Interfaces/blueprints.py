from flask import Blueprint
import app

ecg = Blueprint('ecg', __name__)


def blueprint_register():
	app.app.register_blueprint(ecg, url_prefix='/ecg')

