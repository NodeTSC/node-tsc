from flask import Flask, request
from manager.project_manager import ProjectManager, EdgePortType
from node import NodeFactory, NodeType
import json
from uuid import UUID


app = Flask(__name__)
project = ProjectManager()

@app.route("/")
def index():
    return "Welcome to NodeTSC API!"

@app.route("/project/info", methods=['GET'])
def project_info():
    return project.json()

@app.route("/project/node", methods=['POST', 'PUT', 'DELETE'])
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

@app.route("/project/edge", methods=['POST', 'DELETE'])
def project_edge():
    if request.method == 'POST':
        data = json.loads(request.data)
        project.add_edge(
            source=UUID(data["source"]),
            dest=UUID(data["dest"]),
            port=EdgePortType[data["port-type"]]
        )
        return project.json()
    return "Hi I'm not implemented yet... Sorry..."

@app.route("/project/execute")
async def project_execute():
    data = await project.execute()
    return "Executed..."
