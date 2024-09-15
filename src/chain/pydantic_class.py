from langchain_core.pydantic_v1 import BaseModel, Field

class Hallucination(BaseModel):
    score: bool = Field(description="whether the answer is grounded in supported by a set of facts")
    
class QueryResolver(BaseModel):
    answer: str = Field(description="Answer to the user query based on context")
    slack_post: bool = Field(description="Whether user has asked to post answer to slack in query")