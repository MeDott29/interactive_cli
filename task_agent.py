from openai import OpenAI
from pydantic import BaseModel
from typing import List
import instructor
import datetime

class Task(BaseModel):
    description: str
    beginning: datetime.date

class TaskList(BaseModel):
    tasks: List[Task]

def add_task_to_list(task_list: TaskList, task_description: str):
    if not task_description:
        raise ValueError("Task description cannot be empty")
        
    task = Task(description=task_description)
    task_list.tasks.append(task)


class Assistant:
    def __init__(self):
        self.task_list = TaskList()
        
    def add_task(self, task_description: str):
        add_task_to_list(self, task_description)
        return f"Task '{task_description}' added to your list."

client = OpenAI()
client=instructor.patch(client)

resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": f"today is {datetime.date.today()} Extract task `I want to paint my room tomorrow.`",
        },
    ],
    response_model=TaskList
)
print(resp)
#TaskList.model_validate_json(resp.choices[0].message.function_call.arguments)