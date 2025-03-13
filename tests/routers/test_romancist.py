from http import HTTPStatus

import factory.fuzzy

from madr.models import Romancist


class RomancistFactory(factory.Factory):
    class Meta:
        model = Romancist

    nome = factory.Faker('text')


def test_create_romancist(client):
    response = client.post('/romancists', json={'nome': 'José de alencar'})

    assert response.status_code == HTTPStatus.CREATED


def test_patch_romancist(session, client, token):
    romancist = RomancistFactory()

    session.add(romancist)
    session.commit()

    response = client.patch(
        f'/romancists/{romancist.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': 'José de Alencar'},
    )

    response.status_code == HTTPStatus.OK


def test_find_romancits_by_id(session, client, user, token):
    romancist = RomancistFactory()

    session.add(romancist)
    session.commit()
    session.refresh(romancist)

    response = client.get(
        f'romancists/{romancist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': romancist.id,
        'nome': romancist.nome,
        'created_at': romancist.created_at.isoformat(),
        'updated_at': romancist.updated_at.isoformat(),
    }


def test_delete_romancists(session, client, token):
    romancist = RomancistFactory()

    session.add(romancist)
    session.commit()

    response = client.delete(
        f'/romancists/{romancist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Romancist has been deleted successfully.'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/romancists/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancist not found.'}
