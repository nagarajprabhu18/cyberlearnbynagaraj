import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Category, Course, Lesson, Role

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def override_db():
    with TestingSession() as session:
        yield session


app.dependency_overrides[get_db] = override_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestingSession() as db:
        db.add(Role(name="student"))
        category = Category(name="Networking", slug="networking")
        db.add(category)
        db.flush()
        course = Course(category_id=category.id, title="Network Basics", slug="network-basics", summary="A safe intro to networks", is_published=True)
        db.add(course)
        db.flush()
        db.add(Lesson(course_id=course.id, title="Packets", position=1, content="Packets carry data."))
        db.commit()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as value:
        yield value


async def register_and_login(client):
    created = await client.post("/api/v1/auth/register", json={"email": "learner@example.com", "display_name": "Learner", "password": "safe-learning-password"})
    assert created.status_code == 201
    login = await client.post("/api/v1/auth/login", json={"email": "learner@example.com", "password": "safe-learning-password"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.mark.anyio
async def test_register_login_and_private_dashboard(client):
    headers = await register_and_login(client)
    assert (await client.get("/api/v1/auth/me", headers=headers)).json()["email"] == "learner@example.com"
    assert (await client.get("/api/v1/dashboard", headers=headers)).json() == {"enrolled_courses": 0, "completed_lessons": 0}


@pytest.mark.anyio
async def test_course_enrollment_and_lesson_completion_are_scoped(client):
    headers = await register_and_login(client)
    courses = (await client.get("/api/v1/courses")).json()
    assert courses[0]["title"] == "Network Basics"
    assert (await client.post("/api/v1/lessons/1/complete", headers=headers)).status_code == 403
    assert (await client.post("/api/v1/courses/1/enroll", headers=headers)).status_code == 201
    assert (await client.post("/api/v1/lessons/1/complete", headers=headers)).json()["completed"] is True
    assert (await client.get("/api/v1/dashboard", headers=headers)).json()["completed_lessons"] == 1


@pytest.mark.anyio
async def test_admin_endpoint_rejects_student(client):
    headers = await register_and_login(client)
    assert (await client.get("/api/v1/admin/overview", headers=headers)).status_code == 403


@pytest.mark.anyio
async def test_course_catalog_does_not_expose_lesson_body(client):
    course = (await client.get("/api/v1/courses")).json()[0]
    assert "content" not in course["lessons"][0]


@pytest.mark.anyio
async def test_security_headers_and_password_validation(client):
    response = await client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    rejected = await client.post("/api/v1/auth/register", json={"email": "short@example.com", "display_name": "Short", "password": "short"})
    assert rejected.status_code == 422
