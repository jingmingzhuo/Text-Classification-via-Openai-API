class Task:
    def __init__(self):
        pass
    
    def __len__(self) -> int:
        pass

    def get_input(self, prompt: str, id: int) -> str:
        pass

    def extract_output(self, prompt: str, response: str) -> str:
        pass

    def test_output(self, id: int, output: str) -> bool:
        pass

def get_task(args) ->Task:
    if args.task_name == 'mmlu':
        from .mmlu import MmluTask
        return MmluTask(args.task_file_path)
    if args.task_name == 'sst2':
        from .sst2 import Sst2Task
        return Sst2Task(args.task_file_path)