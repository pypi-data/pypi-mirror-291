import json
class Jsonl:
    def __init__(self, file_path:str):
        self.data=[]
        self.file = file_path
        self._input=""
        self._instruction=""
        self._output=""
        
    @property
    def input(self):
        return self._input
    @input.setter
    def input(self, value):
        self._input = value
    @property
    def instruction(self):
        return self._instruction
    @instruction.setter
    def instruction(self, value):
        self._instruction = value
    @property
    def output(self):
        return self._output
    @output.setter
    def output(self, value):
        self._output = value
    
    @property
    def append(self):
        if len(self.input) > 0 and len(self.instruction) > 0 and len(self.output) > 0:
            self.data.append({"messages":[{"role":"system","content":self.instruction},{"role":"user","content":self.input},{"role":"assistant","content":self.output}]})
            self.input=""
            self.instruction=""
            self.output=""

    @property
    def save(self):
        with open(self.file+".jsonl", 'a+', encoding='utf-8') as f:
            for item in self.data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')