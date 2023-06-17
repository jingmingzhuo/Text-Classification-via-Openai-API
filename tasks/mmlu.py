import re
import pandas as pd
from tasks.task import Task
from prompts.mmlu import *

class MmluTask(Task):
    def __init__(self, file):
        super().__init__()
        self.data = pd.read_csv(file, names=["Text", "A", "B", "C", "D", "Answer"])

    def __len__(self):
        return len(self.data)
    
    def get_input_pure(self, id):
        input = pure_prompt.format(text=self.data["Text"][id], A=self.data["A"][id], B=self.data["B"][id], C=self.data["C"][id], D=self.data["D"][id])
        return input
    
    def get_input_cot(self, id):
        input =  cot_prompt.format(text=self.data["Text"][id], A=self.data["A"][id], B=self.data["B"][id], C=self.data["C"][id], D=self.data["D"][id])
        return input
    
    def get_input(self, prompt: str, id: int) -> str:
        if prompt == 'pure':
            return self.get_input_pure(id)
        else:
            return self.get_input_cot(id)

    def extract_output_pure(self, response):
        pattern = r'^[\w]{1,1}'
        search = re.search(pattern, response)
        if search:
            return search.group(0)
        else:
            return None

    def extract_output_cot(self, response):
        pattern = r'The answer is \((.)\)'
        search = re.search(pattern, response, re.I)
        if search:
            return search.group(1)
        else:
            return None

    def extract_output(self, prompt: str, response: str) -> str:
        if prompt == 'pure':
            return self.extract_output_pure(response)
        else:
            return self.extract_output_cot(response)

    def test_output(self, id, output):
        return self.data["Answer"][id] == output