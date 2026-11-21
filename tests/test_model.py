"""synonyms 核心逻辑测试。"""

import unittest

from synonyms.model import (
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


class SynonymTests(unittest.TestCase):
    def test_known_synonym(self):
        self.assertEqual(synonyms_of("快乐"), ["高兴"])

    def test_reverse_lookup(self):
        self.assertEqual(synonyms_of("高兴"), ["快乐"])

    def test_strips_spaces(self):
        self.assertEqual(synonyms_of(" 美丽 "), ["漂亮"])

    def test_unknown_word(self):
        with self.assertRaises(ValueError):
            synonyms_of("飞机")

    def test_empty_word(self):
        with self.assertRaises(ValueError):
            synonyms_of("   ")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            synonyms_of(1)  # type: ignore[arg-type]

    def test_every_pair_is_searchable(self):
        for left, right in SYNONYM_PAIRS:
            with self.subTest(pair=(left, right)):
                self.assertIn(right, synonyms_of(left))
                self.assertIn(left, synonyms_of(right))


class AntonymTests(unittest.TestCase):
    def test_known_antonym(self):
        self.assertEqual(antonyms_of("大"), ["小"])

    def test_reverse_lookup(self):
        self.assertEqual(antonyms_of("小"), ["大"])

    def test_multi_character(self):
        self.assertEqual(antonyms_of("安全"), ["危险"])

    def test_unknown_word(self):
        with self.assertRaises(ValueError):
            antonyms_of("电脑")

    def test_empty_word(self):
        with self.assertRaises(ValueError):
            antonyms_of("")

    def test_every_pair_is_searchable(self):
        for left, right in ANTONYM_PAIRS:
            with self.subTest(pair=(left, right)):
                self.assertIn(right, antonyms_of(left))
                self.assertIn(left, antonyms_of(right))


class RelationTests(unittest.TestCase):
    def test_is_synonym(self):
        self.assertTrue(is_synonym("快乐", "高兴"))

    def test_is_synonym_reversed(self):
        self.assertTrue(is_synonym("高兴", "快乐"))

    def test_is_synonym_false(self):
        self.assertFalse(is_synonym("快乐", "悲伤"))

    def test_is_antonym(self):
        self.assertTrue(is_antonym("大", "小"))

    def test_is_antonym_reversed(self):
        self.assertTrue(is_antonym("小", "大"))

    def test_is_antonym_false(self):
        self.assertFalse(is_antonym("大", "高"))

    def test_related_both(self):
        data = related("简单")
        self.assertEqual(data["synonyms"], ["容易"])
        self.assertEqual(data["antonyms"], ["复杂"])

    def test_related_only_synonym(self):
        data = related("快乐")
        self.assertEqual(data["synonyms"], ["高兴"])
        self.assertEqual(data["antonyms"], [])

    def test_related_only_antonym(self):
        data = related("大")
        self.assertEqual(data["synonyms"], [])
        self.assertEqual(data["antonyms"], ["小"])

    def test_related_unknown(self):
        data = related("火箭")
        self.assertEqual(data["synonyms"], [])
        self.assertEqual(data["antonyms"], [])

    def test_related_non_string(self):
        with self.assertRaises(TypeError):
            related(None)  # type: ignore[arg-type]


class MatchingQuizTests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(make_matching_quiz(5, seed=1)), 5)

    def test_deterministic(self):
        self.assertEqual(
            make_matching_quiz(5, seed=2), make_matching_quiz(5, seed=2)
        )

    def test_pairs_are_valid(self):
        for left, right in make_matching_quiz(5, seed=3):
            self.assertIn((left, right), SYNONYM_PAIRS)

    def test_zero_count(self):
        with self.assertRaises(ValueError):
            make_matching_quiz(0)

    def test_negative_count(self):
        with self.assertRaises(ValueError):
            make_matching_quiz(-1)

    def test_too_many(self):
        with self.assertRaises(ValueError):
            make_matching_quiz(len(SYNONYM_PAIRS) + 1)

    def test_float_count(self):
        with self.assertRaises(TypeError):
            make_matching_quiz(2.5)  # type: ignore[arg-type]

    def test_bool_count(self):
        with self.assertRaises(TypeError):
            make_matching_quiz(True)  # type: ignore[arg-type]


class AntonymQuizTests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(make_antonym_quiz(4, seed=1)), 4)

    def test_deterministic(self):
        self.assertEqual(
            [q["prompt"] for q in make_antonym_quiz(4, seed=8)],
            [q["prompt"] for q in make_antonym_quiz(4, seed=8)],
        )

    def test_answer_in_choices(self):
        for question in make_antonym_quiz(6, seed=4):
            with self.subTest(prompt=question["prompt"]):
                self.assertIn(question["answer"], question["choices"])

    def test_four_unique_choices(self):
        for question in make_antonym_quiz(6, seed=4):
            self.assertEqual(len(set(question["choices"])), 4)

    def test_answer_is_antonym(self):
        for question in make_antonym_quiz(6, seed=4):
            self.assertTrue(
                is_antonym(str(question["prompt"]), str(question["answer"]))
            )

    def test_zero_count(self):
        with self.assertRaises(ValueError):
            make_antonym_quiz(0)

    def test_too_many(self):
        with self.assertRaises(ValueError):
            make_antonym_quiz(len(ANTONYM_PAIRS) + 1)

    def test_float_count(self):
        with self.assertRaises(TypeError):
            make_antonym_quiz(1.5)  # type: ignore[arg-type]


class GradeTests(unittest.TestCase):
    def setUp(self):
        self.questions = make_antonym_quiz(3, seed=12)

    def test_all_correct(self):
        answers = [str(q["answer"]) for q in self.questions]
        self.assertEqual(
            grade(self.questions, answers),
            {"correct": 3, "total": 3, "score": 100},
        )

    def test_partial(self):
        answers = [str(self.questions[0]["answer"]), "错", "错"]
        result = grade(self.questions, answers)
        self.assertEqual(result["total"], 3)
        self.assertLessEqual(result["correct"], 3)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            grade(self.questions, ["大"])

    def test_empty_questions(self):
        with self.assertRaises(ValueError):
            grade([], [])

    def test_non_string_answer(self):
        with self.assertRaises(TypeError):
            grade(self.questions, [1, 2, 3])  # type: ignore[list-item]

    def test_strips_answers(self):
        answers = [" %s " % q["answer"] for q in self.questions]
        self.assertEqual(grade(self.questions, answers)["correct"], 3)


class WordListTests(unittest.TestCase):
    def test_words_are_sorted(self):
        words = all_words()
        self.assertEqual(words, sorted(words))

    def test_words_are_unique(self):
        words = all_words()
        self.assertEqual(len(words), len(set(words)))

    def test_contains_samples(self):
        words = all_words()
        self.assertIn("快乐", words)
        self.assertIn("大小".replace("大小", "大"), words)

    def test_pair_counts(self):
        self.assertGreaterEqual(len(SYNONYM_PAIRS), 20)
        self.assertGreaterEqual(len(ANTONYM_PAIRS), 20)


if __name__ == "__main__":
    unittest.main()
