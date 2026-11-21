"""synonyms 命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .model import (
    ANTONYM_PAIRS,
    SYNONYM_PAIRS,
    all_words,
    antonyms_of,
    make_antonym_quiz,
    make_matching_quiz,
    related,
    synonyms_of,
)
from .render import matching_html, quiz_html


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="synonyms", description="近义词与反义词：查询、连线题和选择题"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    syn = sub.add_parser("syn", help="查询近义词")
    syn.add_argument("word")

    ant = sub.add_parser("ant", help="查询反义词")
    ant.add_argument("word")

    info = sub.add_parser("info", help="同时查询近义词和反义词")
    info.add_argument("word")

    sub.add_parser("list", help="查看词库规模")

    matching = sub.add_parser("matching", help="生成近义词连线题")
    matching.add_argument("--count", type=int, default=6)
    matching.add_argument("--seed", type=int, default=0)
    matching.add_argument("-o", "--output", required=True)

    quiz = sub.add_parser("quiz", help="生成反义词选择题")
    quiz.add_argument("--count", type=int, default=5)
    quiz.add_argument("--seed", type=int, default=0)
    quiz.add_argument("-o", "--output", required=True)
    quiz.add_argument("--no-answers", action="store_true")

    return parser


def _run(args: argparse.Namespace) -> int:
    if args.command == "syn":
        words = synonyms_of(args.word)
        print("%s 的近义词：%s" % (args.word.strip(), "、".join(words)))
        return 0
    if args.command == "ant":
        words = antonyms_of(args.word)
        print("%s 的反义词：%s" % (args.word.strip(), "、".join(words)))
        return 0
    if args.command == "info":
        data = related(args.word)
        synonyms = "、".join(data["synonyms"]) or "暂无"
        antonyms = "、".join(data["antonyms"]) or "暂无"
        print("%s" % data["word"])
        print("近义词：%s" % synonyms)
        print("反义词：%s" % antonyms)
        return 0
    if args.command == "list":
        print("近义词对：%d 组" % len(SYNONYM_PAIRS))
        print("反义词对：%d 组" % len(ANTONYM_PAIRS))
        print("收录词语：%d 个" % len(all_words()))
        return 0
    if args.command == "matching":
        pairs = make_matching_quiz(args.count, args.seed)
        Path(args.output).write_text(
            matching_html(pairs, seed=args.seed), encoding="utf-8"
        )
        print("已生成连线题：%s（%d 组）" % (args.output, len(pairs)))
        return 0
    if args.command == "quiz":
        questions = make_antonym_quiz(args.count, args.seed)
        Path(args.output).write_text(
            quiz_html(questions, include_answers=not args.no_answers),
            encoding="utf-8",
        )
        print("已生成选择题：%s（%d 题）" % (args.output, len(questions)))
        return 0
    raise ValueError("未知命令：%s" % args.command)


def _ensure_utf8_console() -> None:
    """Windows 控制台默认编码可能无法输出中文，尽量切换为 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            continue


def main(argv: Optional[Sequence[str]] = None) -> int:
    _ensure_utf8_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except (TypeError, ValueError) as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
