from http import HTTPStatus

import factory.fuzzy

from madr.models import Book, Romancist


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    ano = factory.Faker('year')
    titulo = factory.Faker('text')

    romancista_id = 1


class RomancistFactory(factory.Factory):
    class Meta:
        model = Romancist

    nome = factory.Faker('text')


def test_create_book(client, session):
    romancist = RomancistFactory()
    session.add(romancist)
    session.commit()

    response = client.post(
        '/books', json={'ano': 2020, 'titulo': 'Narnia', 'romancista_id': 1}
    )

    assert response.status_code == HTTPStatus.CREATED
