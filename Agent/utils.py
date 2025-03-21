from typing import List
from pydantic import BaseModel, Field


# pydantic model for getting structured output of LLM


class answer(BaseModel):

    KeyAnswer: str = Field(..., description="brife and key answer of a question")


class stanzaList(BaseModel):
    stanzaList: List[str] = Field(
        [],
        description="List of stanzas of a poet",
    )
