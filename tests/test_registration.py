import pytest
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import get_async_session, Base

# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
    echo=True,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_test_session() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


# Override the dependency
app.dependency_overrides[get_async_session] = get_test_session


@pytest.fixture
async def setup_database():
    """Create tables before tests and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(setup_database):
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def sample_tournament_data():
    """Sample tournament data for testing."""
    return {
        "name": "Test Tournament",
        "max_players": 2,
        "start_at": "2025-12-01T15:00:00Z",
    }


@pytest.fixture
async def sample_player_data():
    """Sample player data for testing."""
    return {"name": "John Doe", "email": "john@example.com"}


async def test_create_tournament(client: AsyncClient, sample_tournament_data):
    """Test tournament creation."""
    response = await client.post("/api/v1/tournaments", json=sample_tournament_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_tournament_data["name"]
    assert data["max_players"] == sample_tournament_data["max_players"]
    assert data["registered_players"] == 0
    assert "id" in data


async def test_register_player_success(
    client: AsyncClient, sample_tournament_data, sample_player_data
):
    """Test successful player registration."""
    # Create tournament first
    tournament_response = await client.post(
        "/api/v1/tournaments", json=sample_tournament_data
    )
    tournament_id = tournament_response.json()["id"]

    # Register player
    response = await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=sample_player_data
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_player_data["name"]
    assert data["email"] == sample_player_data["email"]
    assert data["tournament_id"] == tournament_id


async def test_register_player_tournament_not_found(
    client: AsyncClient, sample_player_data
):
    """Test player registration for non-existent tournament."""
    response = await client.post(
        "/api/v1/tournaments/999/register", json=sample_player_data
    )

    assert response.status_code == 404
    assert "Tournament not found" in response.json()["detail"]


async def test_register_player_duplicate_email(
    client: AsyncClient, sample_tournament_data, sample_player_data
):
    """Test duplicate email registration in same tournament."""
    # Create tournament
    tournament_response = await client.post(
        "/api/v1/tournaments", json=sample_tournament_data
    )
    tournament_id = tournament_response.json()["id"]

    # Register player first time
    await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=sample_player_data
    )

    # Try to register same email again
    response = await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=sample_player_data
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


async def test_register_player_tournament_full(
    client: AsyncClient, sample_tournament_data, sample_player_data
):
    """Test player registration when tournament is full."""
    # Create tournament with max 2 players
    tournament_response = await client.post(
        "/api/v1/tournaments", json=sample_tournament_data
    )
    tournament_id = tournament_response.json()["id"]

    # Register first player
    await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=sample_player_data
    )

    # Register second player
    second_player = {"name": "Jane Doe", "email": "jane@example.com"}
    await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=second_player
    )

    # Try to register third player (should fail)
    third_player = {"name": "Bob Smith", "email": "bob@example.com"}
    response = await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=third_player
    )

    assert response.status_code == 400
    assert "Tournament is full" in response.json()["detail"]


async def test_get_tournament_players(
    client: AsyncClient, sample_tournament_data, sample_player_data
):
    """Test getting list of tournament players."""
    # Create tournament
    tournament_response = await client.post(
        "/api/v1/tournaments", json=sample_tournament_data
    )
    tournament_id = tournament_response.json()["id"]

    # Register a player
    await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=sample_player_data
    )

    # Get players list
    response = await client.get(f"/api/v1/tournaments/{tournament_id}/players")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["players"]) == 1
    assert data["players"][0]["name"] == sample_player_data["name"]
    assert data["players"][0]["email"] == sample_player_data["email"]


async def test_get_players_tournament_not_found(client: AsyncClient):
    """Test getting players for non-existent tournament."""
    response = await client.get("/api/v1/tournaments/999/players")

    assert response.status_code == 404
    assert "Tournament not found" in response.json()["detail"]


async def test_invalid_tournament_data(client: AsyncClient):
    """Test tournament creation with invalid data."""
    invalid_data = {
        "name": "",  # Empty name
        "max_players": 0,  # Invalid max_players
        "start_at": "invalid-date",  # Invalid date
    }

    response = await client.post("/api/v1/tournaments", json=invalid_data)
    assert response.status_code == 422


async def test_invalid_player_data(client: AsyncClient, sample_tournament_data):
    """Test player registration with invalid data."""
    # Create tournament first
    tournament_response = await client.post(
        "/api/v1/tournaments", json=sample_tournament_data
    )
    tournament_id = tournament_response.json()["id"]

    invalid_player = {
        "name": "",  # Empty name
        "email": "invalid-email",  # Invalid email
    }

    response = await client.post(
        f"/api/v1/tournaments/{tournament_id}/register", json=invalid_player
    )
    assert response.status_code == 422
