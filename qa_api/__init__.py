from flask import Flask
from qa_api import dispatcher
from qa_api import PC



app = Flask(__name__)
app.config.from_object('apiconfig')
# blueprint here?(flask-restful) or user/dispatcher/PC/(flask-website)     for now user/dispatcher/PC/


app.register_blueprint(dispatcher.mod)
app.register_blueprint(PC.mod)

