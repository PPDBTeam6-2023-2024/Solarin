from pydantic import BaseModel


class PoliticalStanceChange(BaseModel):
    Technocracy: str = "0%"
    Democracy: str = "0%"
    CorporateState: str = "0%"
    Theocracy: str = "0%"
    Anarchism: str = "0%"
    Authoritarian: str = "0%"
    Cost: dict = {}


class PoliticalStanceInput(BaseModel):
    anarchism: float
    authoritarian: float
    democratic: float
    corporate_state: float
    theocracy: float
    technocracy: float
