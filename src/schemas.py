from pydantic import BaseModel
from typing import Optional
from datetime import date

class TeamBase(BaseModel):
    name: str
    full_name: Optional[str] = None
    base_location: Optional[str] = None
    team_principal: Optional[str] = None
    engine_supplier: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    class Config:
        from_attributes = True

class DriverBase(BaseModel):
    first_name: str
    last_name: str
    driver_code: str
    nationality: Optional[str] = None
    permanent_number: int
    is_active: bool = True

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    id: int
    class Config:
        from_attributes = True


class DriverStanding(BaseModel):
    rank: int
    full_name: str
    team_name: str
    total_points: float

class CareerHistory(BaseModel):
    team_name: str
    start_date: date
    end_date: Optional[date] = None
    salary: Optional[float] = None

    class Config:
        from_attributes = True