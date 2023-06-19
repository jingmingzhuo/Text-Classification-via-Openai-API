import re
import pandas as pd
from tasks.task import Task
from prompts.mmlu import *

class MmluTask(Task):
    def __init__(self, file):
        super().__init__()
        self.data = pd.read_csv(file, names=["Text", "A", "B", "C", "D", "Answer"])
        self.steps = 2
        self.stop = ['.']*2

    def __len__(self):
        return len(self.data)
    
    def get_input_pure(self, id):
        input = pure_prompt.format(text=self.data["Text"][id], A=self.data["A"][id], B=self.data["B"][id], C=self.data["C"][id], D=self.data["D"][id])
        return input
    
    def get_input_cot(self, id):
        input = cot_prompt.format(text=self.data["Text"][id], A=self.data["A"][id], B=self.data["B"][id], C=self.data["C"][id], D=self.data["D"][id])
        return input
    
    def get_input_tot(self, id):
        input = proposal_prompt.format(text=self.data["Text"][id], A=self.data["A"][id], B=self.data["B"][id], C=self.data["C"][id], D=self.data["D"][id])
        return input
    
    def get_input_after_tot(self, id, best_thought):
        input = after_tot_prompt.format(text=self.data["Text"][id], A=self.data["A"][id], B=self.data["B"][id], C=self.data["C"][id], D=self.data["D"][id], thoughts=best_thought)
        return input

    def get_input(self, prompt: str, id: int) -> str:
        if prompt == 'pure':
            return self.get_input_pure(id)
        elif prompt == 'cot':
            return self.get_input_cot(id)
        else:
            return self.get_input_tot(id)

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

    def extract_output_tot(self, response):
        pattern = r'^[\w]{1,1}'
        search = re.search(pattern, response)
        if search:
            return search.group(0)
        else:
            return None 

    def extract_output(self, prompt: str, response: str) -> str:
        if prompt == 'pure':
            return self.extract_output_pure(response)
        elif prompt == 'cot':
            return self.extract_output_cot(response)
        else:
            return self.extract_output_tot(response)

    def test_output(self, id, output):
        return self.data["Answer"][id] == output
    
    def get_input_vote(self, id, thoughts):
        prompt = vote_prompt.format(text=self.data["Text"][id])
        for i, thought in enumerate(thoughts, 1):
            prompt += f'Thought {i}: {thought}\n'
        
        prompt += '\nThe best thought is Thought '
        return prompt
    
    def extract_vote(self, response):
        pattern = r'^([\d])'
        search = re.match(pattern, response, re.I)
        if search:
            return int(search.group())
        else:
            return 1