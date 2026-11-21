"""synonyms：近义词与反义词查询及练习生成。"""

from .model import (
    ANTONYM_PAIRS,
    SYNONYM_PAIRS,
    all_words,
    antonyms_of,
    grade,
    is_antonym,
    is_synonym,
    make_antonym_quiz,
    make_matching_quiz,
    related,
    synonyms_of,
)
from .render import matching_html, matching_key_html, quiz_html, quiz_key_html

__all__ = [
    "ANTONYM_PAIRS",
    "SYNONYM_PAIRS",
    "all_words",
    "antonyms_of",
    "grade",
    "is_antonym",
    "is_synonym",
    "make_antonym_quiz",
    "make_matching_quiz",
    "related",
    "synonyms_of",
    "matching_html",
    "matching_key_html",
    "quiz_html",
    "quiz_key_html",
]

__version__ = "0.1.0"
