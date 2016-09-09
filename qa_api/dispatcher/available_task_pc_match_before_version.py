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



import time


parser = reqparse.RequestParser()
parser.add_argument('task', type=str)
parser.add_argument('tracknumber', type=str)
parser.add_argument('status', type=str)




class AvailableTaskPCMatch(Resource):
    def get(self):
        # 创建独立session,为互斥使用
        session = Session()

        ############################################
        ###lock using table machine
        ############################################

        #空闲quality机器列表
        idle_quality_machines = session.query(Machine).with_lockmode('update').filter(Machine.machine_status == 0,
                                                                                      Machine.label == 'quality').all()

        # 空闲linux_compile机器列表
        idle_linux_compile_machines = session.query(Machine).with_lockmode('update').filter(Machine.machine_status == 0,
                                                                                            Machine.label == 'linux_compile').all()

        #机器状态
        machine_dict = {'quality': idle_quality_machines, 'linux_compile': idle_linux_compile_machines}

        #空闲任务（todo doing）
        idle_task_list = session.query(MajorTask).filter(
            or_(MajorTask.task_status == 0, MajorTask.task_status == 1)).all()

        def sub_is_todo(x):
            if x.subtask_status == 0:
                return True
            else:
                return False

        def find_match(machine_dict):
            for major_task in idle_task_list:
                for subtask in filter(sub_is_todo, major_task.subtasks):
                    if len(machine_dict[subtask.label]) == 0:  # this label no machine
                        continue
                    else:
                        target_machine = machine_dict[subtask.label].pop()  # get the target machine
                        return (subtask, target_machine)
            return 0

        find_match_result = find_match(machine_dict)

        if find_match_result != 0:  # get available task machine match success
            '''
            # change the database
            # change the subtask.status from 0 to 1(todo to doing)
            # set subtask.machine_name with the target_machine.hostname
            # change the target_machine.machine_status from 0 to 1(idle to busy)
            # change MajorTask.status,,,before 0 now 1(todo to doing),,,before 1 now 1 or 2(doing to doing or done)
            '''


            # find_match_result[0].subtask_status = 1
            # find_match_result[0].machine_name = find_match_result[1].hostname
            # find_match_result[1].machine_status = 1
            #
            # cur_major = find_match_result[0].MajorTask
            #
            # if cur_major.task_status == 0:#before the Majortask is todo,change it to doing
            #     cur_major.task_status = 1
            #
            # elif cur_major.task_status == 1:#before the Majortask is doing, it is doing
            #     cur_major.task_status = 1#do nothing   password

            ############################################
            ###unlock using table machine
            ############################################

            # time.sleep(10)

            session.commit()

            return {"task name:": find_match_result[0].major_task_name,
                   "subtask_type:": find_match_result[0].subtask_type,
                   "machine:": find_match_result[0].machine_name}

        else:  # find_match_result == 0

            ############################################
            ###unlock using table machine
            ############################################

            session.commit()

            return {"task name:": None, "subtask_type:": None,
                   "machine:": None}








