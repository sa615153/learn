# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apiconfig import DB_URI_local
from apiconfig import DB_URI_linux
from sqlalchemy import create_engine



Base = declarative_base()

class MyMixin(object):
    __table_args__ = {'mysql_engine': 'InnoDB'}



class Machine(MyMixin, Base):
    __tablename__ = 'Machines'

    IP = Column('IPAddress', String(50), primary_key=True, nullable=False)
    status = Column('machine_status', Integer, nullable=False)
    #machine_type = Column('machine_type', Integer)
    label = Column('machine_label', String(50), nullable=False)

    def __repr__(self):
        return "<machine(IPAddress = '%s', machine status = '%s', label = '%s')>" \
               % (self.IP, self.status, self.label)

class MajorTask(MyMixin,Base):
    __tablename__ = 'Tasks'

    track_number = Column('tracknumber', String(100), primary_key=True, nullable=False)
    status = Column('current_status', Integer, nullable=False)
    account = Column('account',String(50), default=None)
    git_dir = Column('gitDir', String(50), nullable=False)
    begin_time = Column('beginTime', String(50), nullable=False)
    is_test2 = Column('isTest2', Integer, default=None)
    is_ideas = Column('isIdeas', Integer, nullable=False)
    saved_tag = Column('savedTag', String(50), default=None)
    comments = Column('comments', String(300), default=None)
    backup_path = Column('backuppath', String(200), default=None)
    suspend = Column('suspend', Integer, default=0)

    subtasks = relationship("SubTask", back_populates="MajorTask")

    def __repr__(self):
        return "<MajorTask(task name = '%s', task status = '%s', account = '%s', git dir = '%s', begin time = '%s' \
        is_test2 = '%s', is_ideas = '%s', saved_tag = '%s', comments = '%s')>"\
               % (self.track_number, self.status, self.account, self.git_dir, self.begin_time, self.is_test2,
                  self.is_ideas, self.saved_tag, self.comments)

class SubTask(MyMixin, Base):
    __tablename__ = 'Subtasks'

    major_task_track_number = Column('tracknumber', String(100), ForeignKey('Tasks.tracknumber'), primary_key=True, nullable=False)
    MajorTask = relationship("MajorTask", back_populates="subtasks")


    name = Column('subtask_name', String(50), primary_key=True, nullable=False)

    status = Column('current_status', Integer, nullable=False)
    benchmark = Column('benchmark', String(100), default=None)
    running_machine = Column('running_machine', String(30), default=None)
    assistant_git_dir = Column('assistant_gitDir', String(50), default=None)
    result = Column('result', String(10), default="unknown")



    def __repr__(self):
        return "<subtask(major_task_track_number = '%s', name = '%s',status = '%s', benchmark = '%s', running_machine = '%s', \
        assistant_git_dir = '%s')>"\
         % (self.major_task_track_number, self.name, self.status, self.benchmark, self.running_machine, self.assistant_git_dir)

class SubtaskNameProperty(MyMixin, Base):
    __tablename__ = 'Subtask_properties'

    subtask_name = Column('subtask_name', String(50), primary_key=True, nullable=False)
    label = Column('available_machine_label', String(50), nullable=False)
    need_benchmark = Column('needBenchmark', Integer, nullable=False)
    need_assistant_git_dir =Column('needAssitantGitDir', Integer, default=None)


    def __repr__(self):
        return "<SubtaskNameProperty(subtask_name = '%s', label = '%s', need_benchmark = '%s', need_assistant_git_dir = \
        '%s')>"\
         % (self.subtask_name, self.label, self.need_benchmark, self.need_assistant_git_dir)




if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine(DB_URI_local, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)






    # print Todo.__table__
    # Base.metadata.create_all(engine)

    # print User.__table__




    # session.add(ed_user)
    # session.commit()


    # u = session.query(User).filter_by(id=3).first()
    # session.delete(u)
    # session.commit()

    # second_user = User(name='second', fullname='second second', password='secondspassword')
    # session.add(second_user)
    # session.commit()






