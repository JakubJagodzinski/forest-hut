from rapidfuzz import process

from src.common_utils import load_json
from src.paths import PATH_JSON_CENSORED_WORDS


class InappropriateContentFilter:
    SIMILARITY_THRESHOLD = 90

    CENSORED_WORD_MASK = '!#@*$'

    CHAR_MAP = {
        '@': 'a',
        '#': 'h',
        '1': 'i',
        '0': 'o',
        '$': 's',
        '3': 'e',
        '!': 'i',
        '|': 'l'
    }

    _censored_words = None

    def __init__(self):
        self.load_censored_words()

    @classmethod
    def load_censored_words(cls):
        cls._censored_words = load_json(PATH_JSON_CENSORED_WORDS)

    @staticmethod
    def normalize_text(text):
        normalized_text = ''
        for char in text:
            if char.lower() in InappropriateContentFilter.CHAR_MAP:
                normalized_text += InappropriateContentFilter.CHAR_MAP[char.lower()]
            else:
                normalized_text += char
        return normalized_text.lower()

    @staticmethod
    def remove_spaces_between_letters(text):
        return ''.join(text.split())

    @staticmethod
    def normalize_and_combine_text(text):
        text_without_spaces = InappropriateContentFilter.remove_spaces_between_letters(text)
        return InappropriateContentFilter.normalize_text(text_without_spaces)

    @classmethod
    def is_similar_to_censored(cls, word, similarity_threshold=90):
        matches = process.extract(word, cls._censored_words, limit=1)
        if matches and matches[0][1] > similarity_threshold:
            return True
        return False

    @classmethod
    def censor_words_in_message(cls, message):
        import re
        words_with_spaces = re.findall(r'\S+|\s+', message)
        censored_message = []
        for word_or_space in words_with_spaces:
            if word_or_space.isspace():
                censored_message.append(word_or_space)
            else:
                normalized_word = InappropriateContentFilter.normalize_and_combine_text(word_or_space)
                if InappropriateContentFilter.is_similar_to_censored(normalized_word):
                    censored_message.append(cls.CENSORED_WORD_MASK)
                else:
                    censored_message.append(word_or_space)
        return ''.join(censored_message)
