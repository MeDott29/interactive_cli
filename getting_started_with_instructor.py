#the first step to solving a problem with instructor is to create a pydantic data model of the problem to be solved
import instructor
from openai import OpenAI
from pydantic import BaseModel

# Enables `response_model`
client = instructor.patch(OpenAI())

class UserDetail(BaseModel):
    name: str
    age: int
user_input=input("Enter the user name")
user = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_model=UserDetail,
    messages=[
        {"role": "user", "content": f"Extract {user_input}"},
    ]
)

assert isinstance(user, UserDetail)
assert user.name == "Jason"
assert user.age == 25