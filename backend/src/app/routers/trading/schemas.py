from pydantic import BaseModel


class TradeOfferSchema(BaseModel):
    offer_id: int
    user_id: int
    gives: list[tuple[str, int]]
    receives: list[tuple[str, int]]
