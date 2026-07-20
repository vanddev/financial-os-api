from datetime import datetime

from pydantic import BaseModel, condecimal, constr

Money = condecimal(max_digits=14, decimal_places=2)


class SettingsBase(BaseModel):
    currency: constr(min_length=1, max_length=8)
    locale: str | None = None
    timezone: str | None = None
    family_name: str | None = None
    emergency_fund_target: Money | None = None


class SettingsCreate(SettingsBase):
    pass


class SettingsOut(SettingsBase):
    id: int
    emergency_fund_target: float | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
