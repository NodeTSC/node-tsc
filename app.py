from flask import Flask, request
from flask_cors import CORS
from manager.project_manager import ProjectManager, EdgePortType
from node import NodeFactory, NodeType
import json
from uuid import UUID
import logging
from utils import NpEncoder


# logging setting
logging.basicConfig(level = logging.INFO)  # showing logging msg

app = Flask(__name__)
CORS(app)  # bypass CORS for all domain
project = ProjectManager()

@app.route("/")
def index():
    return "Welcome to NodeTSC API!"

@app.route("/project/reset")
def reset():
    project.reset()
    return project.json()

@app.route("/project/info", methods=['GET'])
def project_info():
    return project.json()

@app.route("/project/node", methods=['GET', 'POST', 'PUT', 'DELETE'])
def project_node():
    # get node info exception case
    if request.method == 'GET':
        nodeId = UUID(request.args.get("nodeId"))
        node = project.get_node_by_id(nodeId)
        return json.dumps(node.info())
    # other request methods
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
            app.logger.info(f'Create node => {node} with {data["kwargs"]}')
        case 'PUT':
            node = project.get_node_by_id(id_)
            if node is None:
                return "Node Not Found", 404
            node.name = data["name"]
            node.set_parameters(**data["kwargs"])
            app.logger.info(f'Update node => {node} with {data["kwargs"]}')
        case 'DELETE':
            node = project.get_node_by_id(id_)
            if node is None:
                return "Node Not Found", 404
            project.delete_node(node)
            app.logger.info(f'Delete node => {node}')
            return f"Node <id: {id_}> is deleted"
    return node.info()

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

@app.route("/project/save")
def project_save():
    data = json.loads(request.data)
    project.save(data["path"])
    return "saved"

@app.route("/project/load")
def project_load():
    app.logger.info(request.data)
    data = json.loads(request.data)
    app.logger.info(data["path"])
    project.load(data["path"])
    # return project.json()
    return "loaded"

@app.route("/visualize/data", methods=["GET"])
def visualize_data():
    nodeId = UUID(request.args.get("nodeId"))
    return json.dumps(
        project.get_node_by_id(nodeId).get_visualize_data(), cls=NpEncoder
    )
