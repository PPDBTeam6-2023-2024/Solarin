from pydantic import BaseModel


class PoliticalStanceInput(BaseModel):
    anarchism: float
    authoritarian: float
    democratic: float
    corporate_state: float
    theocracy: float
    technocracy: float
