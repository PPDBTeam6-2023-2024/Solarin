from pydantic import BaseModel


class GeneralScheme(BaseModel):
    name: str


class GeneralModifiersScheme(BaseModel):
    stat: str
    modifier: float
    political_stance: str
    political_stance_modifier: float
