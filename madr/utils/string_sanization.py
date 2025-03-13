import re


def remove_special_carecteres(word: str):
    word_to_lower = re.sub(
        r'[^\wáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', word
    ).lower()

    return word_to_lower


def remove_spaces(words: str):
    words_split = words.split()
    replace_spaces = [word.strip() for word in words_split]

    return ' '.join(replace_spaces)


def sanitize_string(words: str):
    new_word = remove_spaces(words)
    new_word = remove_special_carecteres(new_word)

    return new_word
