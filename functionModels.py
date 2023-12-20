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

class FunctionJson(BaseModel):
    name: str = Field(..., description="The name of the function")
    description: str = Field(..., description="The description of the function")
    parameters: FunctionParameters = Field(..., description="The parameters of the function")