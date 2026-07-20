from pydantic import BaseModel


class HistoricalValue(BaseModel):
    month: str
    value: float
