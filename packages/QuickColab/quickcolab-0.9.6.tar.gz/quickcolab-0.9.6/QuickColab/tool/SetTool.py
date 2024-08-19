import json
class ToolCreate:
    def __init__(self):
        self.name = ""
        self.desc = ""
        self.para = {}
        self._require = []

    def set_para(self, name: str, type: str, desc: str):
        self.para = {
            "type": "object",
            "properties": {name: {"type": type, "description": desc}},
        }

    @property
    def require(self):
        return self._require

    @require.setter
    def require(self, value: str):
        self._require.append(value)

    def __call__(self):
        return [{
            
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.desc,
                "parameters": self.para,
                "required": self._require,
            }
        }]