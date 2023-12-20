from node import NodeImpl, DataInput


class PrepNode(NodeImpl, DataInput):
    def __init__(self, project_path: str, name: str = None, **kwargs) -> None:
        super().__init__(project_path, name, **kwargs)
        if name is None:
            self.name = "Prep"
        self.instructions = []
        self.output = {
            "data": None,
            "label": {
                "index": None,
                "target": None
            }
        }
        
    def execute(self):
        self.output["data"] = self.data.get_output("data")
        for i in self.instructions:
            command, column, to = i
            match command:
                case "set_role":
                    self.set_role(column, to)
                case "change_type":
                    self.change_type(column, to)
                    
    def priority(self) -> int:
        return self.data.priority() + 1
    
    def set_instructions(self, instruction: list):
        self.instructions = instruction
    
    def set_role(self, column: str, role: str):
        self.output["label"][role] = column
    
    def change_type(self, column: str, as_type: any):
        self.output["data"][column] = self.output["data"][column].astype(as_type)
