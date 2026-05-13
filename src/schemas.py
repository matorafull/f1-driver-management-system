from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    name: str
    principal: str
    origin: str

class DriverBase(BaseModel):
    first_name: str
    last_name: str
    number: int
    code: str
    team_id: int

class DriverUpdate(BaseModel):
    points: int