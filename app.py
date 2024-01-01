from flask import Flask
from manager.project_manager import ProjectManager

app = Flask(__name__)
project = ProjectManager()

@app.route("/")
def index():
    return "Welcome to NodeTSC API!"

@app.route("/project/info", methods=['GET'])
def project_info():
    return project.json()

@app.route("/project/node", methods=['GET', 'POST', 'PUT', 'DELETE'])
def project_node():
    # TODO: implement node apis
    return "project node create/update/delete"

@app.route("/project/edge", methods=['GET', 'POST', 'DELETE'])
def project_edge():
    # TODO: implement edge apis
    return "project edge create/delete"
