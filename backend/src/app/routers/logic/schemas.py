from pydantic import BaseModel


class PoliticalStanceChange(BaseModel):
    Technocracy: str = "0%"
    Democratic: str = "0%"
    Corporate_State: str = "0%"
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


class ColorCodeScheme(BaseModel):
    primary_color: str
    secondary_color: str
    tertiary_color: str
    text_color: str
