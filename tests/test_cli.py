"""synonyms 命令行测试。"""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from synonyms.cli import main


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class LookupTests(unittest.TestCase):
    def test_syn(self):
        code, out, _ = run(["syn", "快乐"])
        self.assertEqual(code, 0)
        self.assertIn("高兴", out)

    def test_syn_unknown(self):
        code, _, err = run(["syn", "飞机"])
        self.assertEqual(code, 2)
        self.assertIn("没有", err)

    def test_ant(self):
        code, out, _ = run(["ant", "大"])
        self.assertEqual(code, 0)
        self.assertIn("小", out)

    def test_ant_unknown(self):
        code, _, err = run(["ant", "电脑"])
        self.assertEqual(code, 2)
        self.assertIn("没有", err)

    def test_info_both(self):
        code, out, _ = run(["info", "简单"])
        self.assertEqual(code, 0)
        self.assertIn("容易", out)
        self.assertIn("复杂", out)

    def test_info_unknown(self):
        code, out, _ = run(["info", "火箭"])
        self.assertEqual(code, 0)
        self.assertIn("暂无", out)


class ListTests(unittest.TestCase):
    def test_list(self):
        code, out, _ = run(["list"])
        self.assertEqual(code, 0)
        self.assertIn("近义词对", out)
        self.assertIn("反义词对", out)


class MatchingCommandTests(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "match.html"
            code, out, _ = run(["matching", "--count", "5", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("5 组", out)

    def test_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a.html"
            second = Path(tmp) / "b.html"
            run(["matching", "--count", "4", "--seed", "6", "-o", str(first)])
            run(["matching", "--count", "4", "--seed", "6", "-o", str(second)])
            self.assertEqual(
                first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8")
            )

    def test_too_many(self):
        code, _, err = run(["matching", "--count", "99", "-o", "unused.html"])
        self.assertEqual(code, 2)
        self.assertIn("不能超过", err)


class QuizCommandTests(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            code, out, _ = run(["quiz", "--count", "4", "-o", str(output)])
            self.assertEqual(code, 0)
            self.assertTrue(output.exists())
            self.assertIn("4 题", out)

    def test_no_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "quiz.html"
            run(["quiz", "--count", "3", "-o", str(output), "--no-answers"])
            self.assertNotIn("参考答案", output.read_text(encoding="utf-8"))

    def test_zero_count(self):
        code, _, err = run(["quiz", "--count", "0", "-o", "unused.html"])
        self.assertEqual(code, 2)
        self.assertIn("大于 0", err)

    def test_requires_output(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["quiz", "--count", "3"])
        self.assertEqual(ctx.exception.code, 2)


class ParserTests(unittest.TestCase):
    def test_help(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stdout(io.StringIO()):
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_no_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main([])
        self.assertEqual(ctx.exception.code, 2)

    def test_unknown_command(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(io.StringIO()):
                main(["synonym"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
