from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, List

class Property(BaseModel):
    type: str = Field(..., description="The type of the property")

class Properties(BaseModel):
    task_description: Property

class FunctionParameters(BaseModel):
    type: str = Field(..., description="The type of the parameters object")
    properties: Properties = Field(..., description="The properties of the parameters object")
    required: List[str] = Field(..., description="The required properties of the parameters object")

class Function(BaseModel):
    name: str = Field(..., description="The name of the function")
    description: str = Field(..., description="The description of the function")
    parameters: FunctionParameters = Field(..., description="The parameters of the function")

class FunctionJson(BaseModel):
    function: Function

class Tool(BaseModel):
    type: str
    function: Optional[FunctionJson]

class Assistant(BaseModel):
    name: str
    instructions: str
    model: str
    tools: Optional[List[Tool]]
    file_ids: Optional[List[str]]

#This model represents the data needed to create an assistant. The `name`, `instructions`, and `model` fields are required. The `tools` field is a list of `Tool` objects, each of which has a required `type` field and an optional `function` field. The `file_ids` field is an optional list of strings. The `FunctionJson`, `Function`, `FunctionParameters`, `Properties`, and `Property` classes are used to define the structure of a function.

Assistant.model_json_schema()