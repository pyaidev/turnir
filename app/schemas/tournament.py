from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator, ConfigDict
import re


class TournamentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    max_players: int = Field(..., gt=0)
    start_at: datetime


class TournamentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    max_players: int
    start_at: datetime
    registered_players: int


class PlayerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class PlayerRegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    tournament_id: int


class PlayersListResponse(BaseModel):
    players: List[PlayerResponse]
    total: int
