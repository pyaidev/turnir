from typing import List

from fastapi import HTTPException, status

from app.models.tournament import Player, Tournament
from app.repositories.tournament import TournamentRepository
from app.schemas.tournament import (
    PlayerCreate,
    PlayerRegistrationResponse,
    PlayerResponse,
    PlayersListResponse,
    TournamentCreate,
    TournamentResponse,
)


class TournamentService:
    def __init__(self, repository: TournamentRepository) -> None:
        self.repository = repository

    async def create_tournament(
        self, tournament_data: TournamentCreate
    ) -> TournamentResponse:
        tournament = await self.repository.create_tournament(tournament_data)
        return TournamentResponse(
            id=tournament.id,
            name=tournament.name,
            max_players=tournament.max_players,
            start_at=tournament.start_at,
            registered_players=0,
        )

    async def register_player(
        self, tournament_id: int, player_data: PlayerCreate
    ) -> PlayerRegistrationResponse:
        # Check if tournament exists
        tournament = await self.repository.get_tournament_by_id(tournament_id)
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found",
            )

        # Check if player already registered
        if await self.repository.check_player_exists(tournament_id, player_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Player with this email is already registered for this tournament",
            )

        # Check if tournament is full
        current_players = await self.repository.get_players_count(tournament_id)
        if current_players >= tournament.max_players:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tournament is full",
            )

        # Register player
        player = await self.repository.register_player(tournament_id, player_data)
        return PlayerRegistrationResponse(
            id=player.id,
            name=player.name,
            email=player.email,
            tournament_id=player.tournament_id,
        )

    async def get_tournament_players(self, tournament_id: int) -> PlayersListResponse:
        # Check if tournament exists
        tournament = await self.repository.get_tournament_by_id(tournament_id)
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found",
            )

        players = await self.repository.get_tournament_players(tournament_id)
        return PlayersListResponse(
            players=[
                PlayerResponse(id=player.id, name=player.name, email=player.email)
                for player in players
            ],
            total=len(players),
        )
