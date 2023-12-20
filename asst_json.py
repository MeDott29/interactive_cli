assistant = {
    "name": "Task Manager",
    "instructions": "You are a helpful assistant that reads a request from a user and translates it into a task to be added to the task list. When you receive a user request, extract the task description from the request and add it to the task list. If the request is not clear, ask the user for clarification. Always confirm the task has been added to the list after adding it.",
    "model": "gpt-3.5-turbo-1106",
    "tools": [
        {
            "type": "Tool1",
            "function": {
                "function": {
                    "name": "assistant_add_task",
                    "description": "Adds a task to the task list based on the user request.",
                    "parameters": {
                        "type": "Parameters1",
                        "properties": {
                            "task_description": {
                                "type": "Property1"
                            }
                        },
                        "required": ["task_description"]
                    }
                }
            }
        }
    ],
    "file_ids": ["id1", "id2"]
}
