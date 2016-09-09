# -*- coding: utf-8 -*-

from database import Session

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

from qa_api.models import MajorTask
from qa_api.models import Machine
from qa_api.models import SubTask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import or_

parser = reqparse.RequestParser()
parser.add_argument('tracknumber', type=str)
parser.add_argument('machine', type=str)

class IdlePCfinishedTask(Resource):

    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        session = Session()
        parsed_args = parser.parse_args()
        subtask_to_change = session.query(SubTask).filter(SubTask.major_task_track_number == parsed_args["tracknumber"]).first()
        subtask_to_change.status = 2
        subtask_to_change.running_machine = '999'
        machine_to_change = session.query(Machine).filter(Machine.IP == parsed_args["machine"]).first()
        machine_to_change.status = 0

        session.commit()
        return {"PC and subtask status changed":''}
