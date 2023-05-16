"""A singleton to help manage the tasks
Pedro Amaro
"""

class TaskState:
    def __init__(self):
        self.update_count = 0
        self.task = None

taskState = TaskState()