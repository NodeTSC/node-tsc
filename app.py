from flask import Flask, request
from manager.project_manager import ProjectManager
from node import NodeFactory, NodeType
import json

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
    if request.method == 'POST':
        data = json.loads(request.data)
        node = NodeFactory.create_node(
            node_type=NodeType[data["node-type"]],
            name=data["name"],
            **data["kwargs"]
        )
        project.add_node(node)
        return project.json()
    return "Hi I'm not implemented yet... Sorry..."

@app.route("/project/edge", methods=['GET', 'POST', 'DELETE'])
def project_edge():
    # TODO: implement edge apis
    return "project edge create/delete"

@app.route("/project/execute")
def project_execute():
    project.execute()
    return "Executing..."
