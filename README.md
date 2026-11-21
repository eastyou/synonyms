# synonyms

[![CI](https://github.com/eastyou/synonyms/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/synonyms/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

近义词与反义词学习工具：词库查询、连线题和选择题生成。

## 功能

- 24 组近义词、24 组反义词，共收录 90 余个词语
- 支持双向查询：输入任意一侧都能找到对应词
- 同时查询近义词和反义词
- 判断两个词是否构成近义/反义关系
- 生成左右两栏近义词连线题，右栏顺序可复现地打乱
- 生成四选一反义词选择题，自动排除重复选项
- 自动批改并生成百分制成绩
- 输出可直接打印的 HTML 练习页与答案页

## 安装

```bash
pip install -e .
```

也可以直接运行 `python -m synonyms`。

## 使用

```bash
synonyms syn 快乐            # 快乐 的近义词：高兴
synonyms ant 大              # 大 的反义词：小
synonyms info 简单           # 近义词：容易 / 反义词：复杂
synonyms list                # 词库规模

# 近义词连线题
synonyms matching --count 8 --seed 7 -o examples/sheet.html

# 反义词选择题
synonyms quiz --count 6 --seed 3 -o examples/quiz.html
```

## 作为库使用

```python
from synonyms import is_synonym, is_antonym, related, make_antonym_quiz

assert is_synonym("快乐", "高兴")
assert is_antonym("大", "小")
assert related("简单") == {"word": "简单", "synonyms": ["容易"], "antonyms": ["复杂"]}
questions = make_antonym_quiz(3, seed=1)
assert all(len(set(q["choices"])) == 4 for q in questions)
```

## 示例

[examples/sheet.html](examples/sheet.html) 是 8 组近义词连线题，附答案页。

## 测试

```bash
python -m unittest discover -s tests -v
```

共 87 项单元测试，覆盖全部词对的双向查询、关系判断、题目唯一性、可复现随机、批改逻辑和 HTML 转义。CI 覆盖 Python 3.9 ~ 3.13 与三大操作系统。

## 许可

MIT © 2026 eastyou
