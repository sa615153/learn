from flask import Blueprint, render_template, jsonify
from flask_restful import Api
from qa_api.PC.idle_PC_finished_subtask import IdlePCfinishedTask

mod = Blueprint('PC', __name__, url_prefix='/PC')

PC_api = Api(mod)
PC_api.add_resource(IdlePCfinishedTask,'/IdlePCfinishedTask')