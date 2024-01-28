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
    data = json.loads(request.data)
    id_ = None
    try:
        id_ = UUID(data["id"])
    except:
        pass
    match request.method:
        case 'POST':
            node = NodeFactory.create_node(
                node_type=NodeType[data["node-type"]],
                id_=id_,
                name=data["name"],
                **data["kwargs"]
            )
            project.add_node(node)
        case 'PUT':
            node = project.get_node_by_id(id_)
            if node is None:
                return "Node Not Found", 404
            node.set_parameters(**data["kwargs"])
        case 'DELETE':
            node = project.get_node_by_id(id_)
            if node is None:
                return "Node Not Found", 404
            project.delete_node(node)
    return project.json()

@app.route("/project/edge", methods=['POST', 'DELETE'])
def project_edge():
    data = json.loads(request.data)
    action = None
    match request.method:
        case 'POST':
            action = project.add_edge
        case 'DELETE':
            action = project.delete_edge
    action(
        source=UUID(data["source"]),
        dest=UUID(data["dest"]),
        port=EdgePortType[data["port-type"]]
    )
    return project.json()

@app.route("/project/execute")
def project_execute():
    data = project.execute()
    return "Executed..."
