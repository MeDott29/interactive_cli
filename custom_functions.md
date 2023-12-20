The `function_call_how_to.md` file provides a guide on how to use custom functions in an AI Assistant. Here's a summary with relevant code snippets:

1. **Defining a Custom Function**: The document defines a custom function `display_quiz()`. This function takes a `title` and an array of `questions`, displays the quiz, and gets user input for each question.

```python
def display_quiz(title, questions):
    print("Quiz:", title)
    print()
    responses = []

    for q in questions:
        print(q["question_text"])
        response = ""

        # If multiple choice, print options
        if q["question_type"] == "MULTIPLE_CHOICE":
            for i, choice in enumerate(q["choices"]):
                print(f"{i}. {choice}")
            response = get_mock_response_from_user_multiple_choice()

        # Otherwise, just get response
        elif q["question_type"] == "FREE_RESPONSE":
            response = get_mock_response_from_user_free_response()

        responses.append(response)
        print()

    return responses
```

2. **Calling the Custom Function**: The function is then called with a title and a list of questions.

```python
responses = display_quiz(
    "Sample Quiz",
    [
        {"question_text": "What is your name?", "question_type": "FREE_RESPONSE"},
        {
            "question_text": "What is your favorite color?",
            "question_type": "MULTIPLE_CHOICE",
            "choices": ["Red", "Blue", "Green", "Yellow"],
        },
    ],
)
print("Responses:", responses)
```

3. **Defining the Function Interface in JSON**: The interface of the function is defined in JSON format so the Assistant can call it.

```python
function_json = {
    "name": "display_quiz",
    "description": "Displays a quiz to the student, and returns the student's response. A single quiz can have multiple questions.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "questions": {
                "type": "array",
                "description": "An array of questions, each with a title and potentially options (if multiple choice).",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_text": {"type": "string"},
                        "question_type": {
                            "type": "string",
                            "enum": ["MULTIPLE_CHOICE", "FREE_RESPONSE"],
                        },
                        "choices": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["question_text"],
                },
            },
        },
        "required": ["title", "questions"],
    },
}
```

4. **Submitting Function Output**: After calling the function and getting the responses, the responses are submitted back to the Assistant.

```python
run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=[
        {
            "tool_call_id": tool_call.id,
            "output": json.dumps(responses),
        }
    ],
)
```

5. **Waiting for the Run to Complete**: Finally, the document waits for the run to complete and checks the thread.

```python
run = wait_on_run(run, thread)
pretty_print(get_response(thread))
```

This guide provides a comprehensive overview of how to define, call, and manage custom functions in an AI Assistant.
