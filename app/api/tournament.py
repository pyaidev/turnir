from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.repositories.tournament import TournamentRepository
from app.schemas.tournament import (
    PlayerCreate,
    PlayerRegistrationResponse,
    PlayersListResponse,
    TournamentCreate,
    TournamentResponse,
)
from app.services.tournament import TournamentService

router = APIRouter()


def get_tournament_service(
    session: AsyncSession = Depends(get_async_session),
) -> TournamentService:
    repository = TournamentRepository(session)
    return TournamentService(repository)


@router.post(
    "/tournaments",
    response_model=TournamentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tournament(
    tournament_data: TournamentCreate,
    service: TournamentService = Depends(get_tournament_service),
) -> TournamentResponse:
    """Create a new tournament."""
    return await service.create_tournament(tournament_data)


@router.post(
    "/tournaments/{tournament_id}/register",
    response_model=PlayerRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_player(
    tournament_id: int,
    player_data: PlayerCreate,
    service: TournamentService = Depends(get_tournament_service),
) -> PlayerRegistrationResponse:
    """Register a player for a tournament."""
    return await service.register_player(tournament_id, player_data)


@router.get("/tournaments/{tournament_id}/players", response_model=PlayersListResponse)
async def get_tournament_players(
    tournament_id: int,
    service: TournamentService = Depends(get_tournament_service),
) -> PlayersListResponse:
    """Get list of registered players for a tournament."""
    return await service.get_tournament_players(tournament_id)
