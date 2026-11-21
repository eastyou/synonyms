"""近义词与反义词词库、查询和练习生成。"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Tuple

SYNONYM_PAIRS: Tuple[Tuple[str, str], ...] = (
    ("快乐", "高兴"),
    ("美丽", "漂亮"),
    ("寒冷", "严寒"),
    ("立刻", "马上"),
    ("著名", "有名"),
    ("安静", "宁静"),
    ("经常", "常常"),
    ("喜欢", "喜爱"),
    ("仔细", "认真"),
    ("勇敢", "英勇"),
    ("聪明", "伶俐"),
    ("突然", "忽然"),
    ("帮助", "帮忙"),
    ("表扬", "赞扬"),
    ("难过", "伤心"),
    ("简单", "容易"),
    ("洁白", "雪白"),
    ("宽阔", "宽广"),
    ("茂盛", "繁茂"),
    ("珍贵", "宝贵"),
    ("温和", "温柔"),
    ("奇怪", "古怪"),
    ("遥远", "辽远"),
    ("整洁", "干净"),
)

ANTONYM_PAIRS: Tuple[Tuple[str, str], ...] = (
    ("大", "小"),
    ("高", "低"),
    ("冷", "热"),
    ("快", "慢"),
    ("早", "晚"),
    ("多", "少"),
    ("前", "后"),
    ("左", "右"),
    ("黑", "白"),
    ("开", "关"),
    ("真", "假"),
    ("美", "丑"),
    ("新", "旧"),
    ("轻", "重"),
    ("远", "近"),
    ("明", "暗"),
    ("进", "退"),
    ("安全", "危险"),
    ("复杂", "简单"),
    ("勤劳", "懒惰"),
    ("善良", "凶恶"),
    ("潮湿", "干燥"),
    ("骄傲", "谦虚"),
    ("浪费", "节约"),
)

LETTERS = ("A", "B", "C", "D")


def _require_word(word: object) -> str:
    if not isinstance(word, str):
        raise TypeError("词语必须是字符串")
    text = word.strip()
    if not text:
        raise ValueError("词语不能为空")
    return text


def _match(word: str, pairs: Sequence[Tuple[str, str]]) -> List[str]:
    results: List[str] = []
    for left, right in pairs:
        if word == left:
            results.append(right)
        elif word == right:
            results.append(left)
    return results


def synonyms_of(word: str) -> List[str]:
    """返回词语的近义词；查不到时给出明确错误。"""
    text = _require_word(word)
    results = _match(text, SYNONYM_PAIRS)
    if not results:
        raise ValueError("词库中没有“%s”的近义词" % text)
    return results


def antonyms_of(word: str) -> List[str]:
    """返回词语的反义词；查不到时给出明确错误。"""
    text = _require_word(word)
    results = _match(text, ANTONYM_PAIRS)
    if not results:
        raise ValueError("词库中没有“%s”的反义词" % text)
    return results


def is_synonym(first: str, second: str) -> bool:
    """判断两个词是否为一组近义词（顺序无关）。"""
    a = _require_word(first)
    b = _require_word(second)
    return (a, b) in SYNONYM_PAIRS or (b, a) in SYNONYM_PAIRS


def is_antonym(first: str, second: str) -> bool:
    """判断两个词是否为一组反义词（顺序无关）。"""
    a = _require_word(first)
    b = _require_word(second)
    return (a, b) in ANTONYM_PAIRS or (b, a) in ANTONYM_PAIRS


def related(word: str) -> Dict[str, object]:
    """同时查询近义词和反义词，任意一侧不存在时返回空列表。"""
    text = _require_word(word)
    return {
        "word": text,
        "synonyms": _match(text, SYNONYM_PAIRS),
        "antonyms": _match(text, ANTONYM_PAIRS),
    }


def make_matching_quiz(
    count: int = 6, seed: Optional[int] = None
) -> List[Tuple[str, str]]:
    """生成近义词连线题，抽取固定数量的词对。"""
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("题目数量必须是整数")
    if count <= 0:
        raise ValueError("题目数量必须大于 0")
    if count > len(SYNONYM_PAIRS):
        raise ValueError("题目数量不能超过 %d" % len(SYNONYM_PAIRS))
    rng = random.Random(seed)
    return rng.sample(list(SYNONYM_PAIRS), count)


def make_antonym_quiz(
    count: int = 5, seed: Optional[int] = None
) -> List[Dict[str, object]]:
    """生成反义词选择题，每题四个选项且只有一个正确答案。"""
    if isinstance(count, bool) or not isinstance(count, int):
        raise TypeError("题目数量必须是整数")
    if count <= 0:
        raise ValueError("题目数量必须大于 0")
    if count > len(ANTONYM_PAIRS):
        raise ValueError("题目数量不能超过 %d" % len(ANTONYM_PAIRS))
    rng = random.Random(seed)
    pairs = rng.sample(list(ANTONYM_PAIRS), count)
    pool = sorted({word for pair in ANTONYM_PAIRS for word in pair})
    questions: List[Dict[str, object]] = []
    for left, right in pairs:
        prompt, answer = (left, right) if rng.random() < 0.5 else (right, left)
        distractors = [word for word in pool if word not in (prompt, answer)]
        choices = rng.sample(distractors, 3) + [answer]
        rng.shuffle(choices)
        questions.append({"prompt": prompt, "answer": answer, "choices": choices})
    return questions


def grade(
    questions: Sequence[Dict[str, object]], answers: Sequence[str]
) -> Dict[str, int]:
    """按顺序批改选择题。"""
    if not questions:
        raise ValueError("没有可批改的题目")
    if len(questions) != len(answers):
        raise ValueError("答案数量与题目数量不一致")
    correct = 0
    for question, answer in zip(questions, answers):
        if not isinstance(answer, str):
            raise TypeError("答案必须是字符串")
        if answer.strip() == str(question["answer"]).strip():
            correct += 1
    total = len(questions)
    return {"correct": correct, "total": total, "score": round(correct * 100 / total)}


def all_words() -> List[str]:
    """返回词库中的全部词语（去重排序）。"""
    words = {word for pair in SYNONYM_PAIRS + ANTONYM_PAIRS for word in pair}
    return sorted(words)
