import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from madr.app import app
from madr.database import get_session
from madr.models import User, table_registry
from madr.security import get_password_hashed


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:  # Executar os testes de forma isolada
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)

    return engine


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


# @pytest.fixture(scope='session')
# def engine():
#     _engine = create_engine(
#         'sqlite:///:memory:',
#         connect_args={
#             'check_same_thread': False
#         },  # Necessário para SQLite em memória com múltiplas conexões
#         poolclass=StaticPool,
#     )

#     return _engine


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hashed(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hashed(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
