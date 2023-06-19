import pandas as pd
from tasks.task import Task
from prompts.sst2 import *

class Sst2Task(Task):
    def __init__(self, file):
        super().__init__()
        self.data = pd.read_csv(file, sep='\t', header=0)

    def __len__(self):
        return len(self.data)
    
    def get_input_pure(self, id):
        input = pure_prompt.format(text=self.data["sentence"][id])
        return input
    
    def get_input_few_shot(self, id):
        input = few_shot_prompt.format(text=self.data["sentence"][id])
        return input

    def get_input(self, prompt: str, id: int) -> str:
        if prompt == 'pure':
            return self.get_input_pure(id)
        else:
            return self.get_input_few_shot(id)

    def extract_output(self, prompt, response):
        if 'negative' in response or 'Negative' in response:
            return 0
        if 'positive' in response or 'Positive' in response:
            return 1
        return None

    def test_output(self, id, output):
        return int(self.data["label"][id]) == output