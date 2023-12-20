### Functions

As a final powerful tool for your Assistant, you can specify custom [Functions](https://platform.openai.com/docs/assistants/tools/function-calling) (much like the [Function Calling](https://platform.openai.com/docs/guides/function-calling) in the Chat Completions API). During a Run, the Assistant can then indicate it wants to call one or more functions you specified. You are then responsible for calling the Function, and providing the output back to the Assistant.

Let's take a look at an example by defining a `display_quiz()` Function for our Math Tutor.

This function will take a `title` and an array of `question`s, display the quiz, and get input from the user for each:

- `title`
- `questions`
  - `question_text`
  - `question_type`: [`MULTIPLE_CHOICE`, `FREE_RESPONSE`]
  - `choices`: ["choice 1", "choice 2", ...]

```
def get_mock_response_from_user_multiple_choice():
    return "a"


def get_mock_response_from_user_free_response():
    return "I don't know."


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

Here's what a sample quiz would look like:
```
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
Now, let's define the interface of this function in JSON format, so our Assistant can call it:
```
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
Update Assistant
```
assistant = client.beta.assistants.update(
    MATH_ASSISTANT_ID,
    tools=[
        {"type": "code_interpreter"},
        {"type": "retrieval"},
        {"type": "function", "function": function_json},
    ],
)
show_json(assistant)
```
{'id': 'asst_9HAjl9y41ufsViNcThW1EXUS',
 'created_at': 1699828331,
 'description': None,
 'file_ids': ['file-MdXcQI8OdPp76wukWI4dpLwW'],
 'instructions': 'You are a personal math tutor. Answer questions briefly, in a sentence or less.',
 'metadata': {},
 'model': 'gpt-4-1106-preview',
 'name': 'Math Tutor',
 'object': 'assistant',
 'tools': [{'type': 'code_interpreter'},
  {'type': 'retrieval'},
  {'function': {'name': 'display_quiz',
    'parameters': {'type': 'object',
     'properties': {'title': {'type': 'string'},
      'questions': {'type': 'array',
       'description': 'An array of questions, each with a title and potentially options (if multiple choice).',
       'items': {'type': 'object',
        'properties': {'question_text': {'type': 'string'},
         'question_type': {'type': 'string',
          'enum': ['MULTIPLE_CHOICE', 'FREE_RESPONSE']},
         'choices': {'type': 'array', 'items': {'type': 'string'}}},
        'required': ['question_text']}}},
     'required': ['title', 'questions']},
    'description': "Displays a quiz to the student, and returns the student's response. A single quiz can have multiple questions."},
   'type': 'function'}]}

Ask for a quiz
```
thread, run = create_thread_and_run(
    "Make a quiz with 2 questions: One open ended, one multiple choice. Then, give me feedback for the responses."
)
run = wait_on_run(run, thread)
run.status
```
Now, however, when we check the Run's `status` we see `requires_action`!
```
show_json(run)
```
{'id': 'run_98PGE3qGtHoaWaCLoytyRUBf',
 'assistant_id': 'asst_9HAjl9y41ufsViNcThW1EXUS',
 'cancelled_at': None,
 'completed_at': None,
 'created_at': 1699828370,
 'expires_at': 1699828970,
 'failed_at': None,
 'file_ids': ['file-MdXcQI8OdPp76wukWI4dpLwW'],
 'instructions': 'You are a personal math tutor. Answer questions briefly, in a sentence or less.',
 'last_error': None,
 'metadata': {},
 'model': 'gpt-4-1106-preview',
 'object': 'thread.run',
 'required_action': {'submit_tool_outputs': {'tool_calls': [{'id': 'call_Zf650sWT1wW4Uwbf5YeDS0VG',
     'function': {'arguments': '{\n  "title": "Mathematics Quiz",\n  "questions": [\n    {\n      "question_text": "Explain why the square root of a negative number is not a real number.",\n      "question_type": "FREE_RESPONSE"\n    },\n    {\n      "question_text": "What is the value of an angle in a regular pentagon?",\n      "choices": [\n        "72 degrees",\n        "90 degrees",\n        "108 degrees",\n        "120 degrees"\n      ],\n      "question_type": "MULTIPLE_CHOICE"\n    }\n  ]\n}',
      'name': 'display_quiz'},
     'type': 'function'}]},
  'type': 'submit_tool_outputs'},
 'started_at': 1699828370,
 'status': 'requires_action',
 'thread_id': 'thread_bICTESFvWoRdj0O0SzsosLCS',
 'tools': [{'type': 'code_interpreter'},
  {'type': 'retrieval'},
  {'function': {'name': 'display_quiz',
    'parameters': {'type': 'object',
     'properties': {'title': {'type': 'string'},
      'questions': {'type': 'array',
       'description': 'An array of questions, each with a title and potentially options (if multiple choice).',
       'items': {'type': 'object',
        'properties': {'question_text': {'type': 'string'},
         'question_type': {'type': 'string',
          'enum': ['MULTIPLE_CHOICE', 'FREE_RESPONSE']},
         'choices': {'type': 'array', 'items': {'type': 'string'}}},
        'required': ['question_text']}}},
     'required': ['title', 'questions']},
    'description': "Displays a quiz to the student, and returns the student's response. A single quiz can have multiple questions."},
   'type': 'function'}]}

The `required_action` field indicates a Tool is waiting for us to run it and submit its output back to the Assistant. Specifically, the `display_quiz` function! Let's start by parsing the `name` and `arguments`.

> **Note**
> While in this case we know there is only one Tool call, in practice the Assistant may choose to call multiple tools.

```
# Extract single tool call
tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

print("Function Name:", name)
print("Function Arguments:")
arguments
```
Function Name: display_quiz
Function Arguments:
{'title': 'Mathematics Quiz',
 'questions': [{'question_text': 'Explain why the square root of a negative number is not a real number.',
   'question_type': 'FREE_RESPONSE'},
  {'question_text': 'What is the value of an angle in a regular pentagon?',
   'choices': ['72 degrees', '90 degrees', '108 degrees', '120 degrees'],
   'question_type': 'MULTIPLE_CHOICE'}]}
Now let's actually call our `display_quiz` function with the arguments provided by the Assistant:
```
responses = display_quiz(arguments["title"], arguments["questions"])
print("Responses:", responses)
```
Quiz: Mathematics Quiz

Explain why the square root of a negative number is not a real number.

What is the value of an angle in a regular pentagon?
0. 72 degrees
1. 90 degrees
2. 108 degrees
3. 120 degrees

Responses: ["I don't know.", 'a']

Great! (Remember these responses are the one's we mocked earlier. In reality, we'd be getting input from the back from this function call.)

Now that we have our responses, let's submit them back to the Assistant. We'll need the `tool_call` ID, found in the `tool_call` we parsed out earlier. We'll also need to encode our `list`of responses into a `str`.

```
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
show_json(run)
```
{'id': 'run_98PGE3qGtHoaWaCLoytyRUBf',
 'assistant_id': 'asst_9HAjl9y41ufsViNcThW1EXUS',
 'cancelled_at': None,
 'completed_at': None,
 'created_at': 1699828370,
 'expires_at': 1699828970,
 'failed_at': None,
 'file_ids': ['file-MdXcQI8OdPp76wukWI4dpLwW'],
 'instructions': 'You are a personal math tutor. Answer questions briefly, in a sentence or less.',
 'last_error': None,
 'metadata': {},
 'model': 'gpt-4-1106-preview',
 'object': 'thread.run',
 'required_action': None,
 'started_at': 1699828370,
 'status': 'queued',
 'thread_id': 'thread_bICTESFvWoRdj0O0SzsosLCS',
 'tools': [{'type': 'code_interpreter'},
  {'type': 'retrieval'},
  {'function': {'name': 'display_quiz',
    'parameters': {'type': 'object',
     'properties': {'title': {'type': 'string'},
      'questions': {'type': 'array',
       'description': 'An array of questions, each with a title and potentially options (if multiple choice).',
       'items': {'type': 'object',
        'properties': {'question_text': {'type': 'string'},
         'question_type': {'type': 'string',
          'enum': ['MULTIPLE_CHOICE', 'FREE_RESPONSE']},
         'choices': {'type': 'array', 'items': {'type': 'string'}}},
        'required': ['question_text']}}},
     'required': ['title', 'questions']},
    'description': "Displays a quiz to the student, and returns the student's response. A single quiz can have multiple questions."},
   'type': 'function'}]}

We can now wait for the Run to complete once again, and check our Thread!
```
run = wait_on_run(run, thread)
pretty_print(get_response(thread))
```
# Messages
user: Make a quiz with 2 questions: One open ended, one multiple choice. Then, give me feedback for the responses.
assistant: Thank you for attempting the quiz.

For the first question, it's important to know that the square root of a negative number is not a real number because real numbers consist of all the numbers on the number line, and that includes all positive numbers, zero, and negative numbers. However, the square root of a negative number is not on this number line; instead, it is what we call an imaginary number. When we want to take the square root of a negative number, we typically use the imaginary unit \(i\), where \(i\) is defined as \(\sqrt{-1}\).

For the second question, the correct answer is "108 degrees." In a regular pentagon, which is a five-sided polygon with equal sides and angles, each interior angle is \(108\) degrees. This is because the sum of the interior angles of a pentagon is \(540\) degrees, and when divided by \(5\) (the number of angles), it gives \(108\) degrees per angle. The choice you selected, "72 degrees," actually refers to the external angle of a regular pentagon, not the internal angle.
