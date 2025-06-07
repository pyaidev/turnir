from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.tournament import Player, Tournament
from app.schemas.tournament import PlayerCreate, TournamentCreate


class TournamentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_tournament(self, tournament_data: TournamentCreate) -> Tournament:
        tournament = Tournament(
            name=tournament_data.name,
            max_players=tournament_data.max_players,
            start_at=tournament_data.start_at,
        )
        self.session.add(tournament)
        await self.session.commit()
        await self.session.refresh(tournament)
        return tournament

    async def get_tournament_by_id(self, tournament_id: int) -> Optional[Tournament]:
        stmt = select(Tournament).where(Tournament.id == tournament_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_tournament_with_players(
        self, tournament_id: int
    ) -> Optional[Tournament]:
        stmt = (
            select(Tournament)
            .options(selectinload(Tournament.players))
            .where(Tournament.id == tournament_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_players_count(self, tournament_id: int) -> int:
        stmt = select(func.count(Player.id)).where(
            Player.tournament_id == tournament_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def register_player(
        self, tournament_id: int, player_data: PlayerCreate
    ) -> Player:
        player = Player(
            name=player_data.name,
            email=player_data.email,
            tournament_id=tournament_id,
        )
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def check_player_exists(self, tournament_id: int, email: str) -> bool:
        stmt = select(Player).where(
            Player.tournament_id == tournament_id, Player.email == email
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_tournament_players(self, tournament_id: int) -> List[Player]:
        stmt = select(Player).where(Player.tournament_id == tournament_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
