import pytest
from madr.utils.string_sanization import remove_special_carecteres, remove_spaces



def test_remove_special_carecteres():

    word = "Androides Sonham Com Ovelhas Elétricas?"

    new_word = remove_special_carecteres(word)

    assert new_word == 'androides sonham com ovelhas elétricas'


def test_remove_spaces():

    word = "  breve  história  do tempo "

    new_word = remove_spaces(word)

    assert new_word == 'breve história do tempo'

