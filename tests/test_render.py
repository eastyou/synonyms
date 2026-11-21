"""synonyms 渲染测试。"""

import unittest

from synonyms.model import make_antonym_quiz, make_matching_quiz
from synonyms.render import matching_html, matching_key_html, quiz_html, quiz_key_html

PAIRS = make_matching_quiz(4, seed=1)
QUESTIONS = make_antonym_quiz(3, seed=2)


class MatchingTests(unittest.TestCase):
    def test_full_document(self):
        page = matching_html(PAIRS)
        self.assertTrue(page.startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", page)

    def test_contains_left_words(self):
        page = matching_html(PAIRS)
        for left, _ in PAIRS:
            self.assertIn(left, page)

    def test_contains_right_words(self):
        page = matching_html(PAIRS)
        for _, right in PAIRS:
            self.assertIn(right, page)

    def test_contains_answers(self):
        page = matching_html(PAIRS)
        self.assertIn("参考答案", page)

    def test_can_hide_answers(self):
        page = matching_html(PAIRS, include_answers=False)
        self.assertNotIn("参考答案", page)

    def test_custom_title(self):
        page = matching_html(PAIRS, title="三年级词语练习")
        self.assertIn("三年级词语练习", page)

    def test_escapes_html(self):
        page = matching_html([("<b>", "<i>")])
        self.assertNotIn("<b>", page)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            matching_html([])

    def test_seed_changes_order(self):
        first = matching_html(PAIRS, seed=1)
        second = matching_html(PAIRS, seed=99)
        self.assertNotEqual(first, second)


class QuizTests(unittest.TestCase):
    def test_full_document(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("<!DOCTYPE html>", page)

    def test_contains_prompts(self):
        page = quiz_html(QUESTIONS)
        for question in QUESTIONS:
            self.assertIn(str(question["prompt"]), page)

    def test_contains_options(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("type=\"radio\"", page)

    def test_contains_answers(self):
        page = quiz_html(QUESTIONS)
        self.assertIn("参考答案", page)

    def test_can_hide_answers(self):
        page = quiz_html(QUESTIONS, include_answers=False)
        self.assertNotIn("参考答案", page)

    def test_custom_title(self):
        page = quiz_html(QUESTIONS, title="反义词专项")
        self.assertIn("反义词专项", page)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            quiz_html([])


class KeyTests(unittest.TestCase):
    def test_matching_key(self):
        key = matching_key_html(PAIRS)
        self.assertIn("<ol", key)
        first = PAIRS[0][0]
        self.assertIn(first, key)

    def test_matching_key_empty(self):
        with self.assertRaises(ValueError):
            matching_key_html([])

    def test_quiz_key(self):
        key = quiz_key_html(QUESTIONS)
        self.assertIn("1.", key)
        self.assertIn(str(QUESTIONS[0]["answer"]), key)

    def test_quiz_key_empty(self):
        with self.assertRaises(ValueError):
            quiz_key_html([])


if __name__ == "__main__":
    unittest.main()
