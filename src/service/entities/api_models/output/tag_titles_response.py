from typing import List

from pydantic import BaseModel


class TagTitlesResponse(BaseModel):
    tags: List[str]
