#!/usr/bin/env python3
"""The Project 4 autograder harness. PROVIDED FILE, DO NOT MODIFY.

    python3 tests/grade_p4.py <case>

The autograder runs this once per test, and check.py runs it the same way. It
imports your leaderboard.py, calls your functions on files it writes into a
temporary folder, and exits 0 when every result is exactly right. When one is
not, it prints what it expected and what it got.

Cases:
    load_questions        two question files
    load_questions_edges  empty, one line, an odd line count, no final newline
    save_score            saves onto an existing file and onto an empty one
    load_scores           two score files
    display               two leaderboards, one with a tie
    engine                two games played through quiz_engine.py

Before any test runs, the autograder checks that this file, quiz_engine.py,
questions.txt and the concept checker are exactly as provided. Editing any of
them scores every test 0.
"""
import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADER = "=== Leaderboard ==="


class Fail(Exception):
    """A test failed; the message says why."""


def write_file(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def read_file(path):
    # Text mode, so a line ending written as \r\n on Windows reads as \n and
    # check.py agrees with the autograder, which runs on Linux.
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def show(text):
    """A file's contents or a value, spelled out so newlines are visible."""
    return "    " + repr(text)


def show_lines(lines):
    if not lines:
        return "    (nothing)"
    return "\n".join("    " + text for text in lines)


def output_lines(printed):
    """Printed text as lines, trailing spaces and one trailing blank ignored."""
    lines = [text.rstrip() for text in printed.splitlines()]
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def exact(got, want):
    """Equal in value AND in type, all the way down, so a value whose own
    == always says yes cannot pass for the right answer."""
    if type(got) is not type(want):
        return False
    if isinstance(want, list):
        return len(got) == len(want) and all(
            exact(a, b) for a, b in zip(got, want))
    return got == want


def load_student():
    # Loaded by path, and the repository is never put on sys.path, so no other
    # file in it can be imported, whether by name, by help() or by pydoc.
    sys.stdin = io.StringIO("")
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            spec = importlib.util.spec_from_file_location(
                "leaderboard", os.path.join(ROOT, "leaderboard.py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules["leaderboard"] = module
            spec.loader.exec_module(module)
            return module
    except EOFError:
        raise Fail("leaderboard.py asked for input as soon as it was imported. "
                   "Everything at the top level of the file runs on import, so "
                   "only your header comment and function definitions belong "
                   "there.")
    except SyntaxError as err:
        raise Fail("leaderboard.py does not run. SyntaxError on line %s: %s"
                   % (err.lineno, err.msg))
    except (Exception, SystemExit) as err:
        raise Fail("Importing leaderboard.py raised %s: %s"
                   % (type(err).__name__, err))


def function(module, name):
    func = getattr(module, name, None)
    if not callable(func):
        raise Fail("leaderboard.py has no function named " + name + ".")
    return func


def call(func, what, *args):
    """Call a student function. Returns (result, printed text)."""
    printed = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed):
            result = func(*args)
    except EOFError:
        raise Fail(what + " asked for input. None of the four functions reads "
                   "from the keyboard.")
    except (Exception, SystemExit) as err:
        raise Fail("%s raised %s: %s" % (what, type(err).__name__, err))
    return result, printed.getvalue()


def as_pairs(result, what):
    if not isinstance(result, list):
        raise Fail(what + " returned\n" + show(result)
                   + "\nwhich is not a list.")
    pairs = []
    for item in result:
        if not isinstance(item, (list, tuple)):
            raise Fail(what + " returned\n" + show(result) + "\nand the item "
                       + repr(item) + " is not a pair.")
        pairs.append(list(item))
    return pairs


# ------------------------------------------------------------------ cases ---

QUESTION_FILES = [
    ("Which planet is closest to the Sun?\nMercury\n"
     "How many legs does a spider have?\n8\n"
     "Who wrote Romeo and Juliet?\nWilliam Shakespeare\n",
     [["Which planet is closest to the Sun?", "Mercury"],
      ["How many legs does a spider have?", "8"],
      ["Who wrote Romeo and Juliet?", "William Shakespeare"]]),
    ("What color do you get by mixing blue and yellow?\ngreen\n"
     "What is 12 divided by 4?\n3\n",
     [["What color do you get by mixing blue and yellow?", "green"],
      ["What is 12 divided by 4?", "3"]]),
]

QUESTION_EDGES = [
    ("", []),
    ("What is the tallest mountain on Earth?\n", []),
    ("What is 9 plus 10?\n19\nWhat is the boiling point of water in Celsius?\n",
     [["What is 9 plus 10?", "19"]]),
    ("Name a primary color.\nred\nWhat is 5 squared?\n25",
     [["Name a primary color.", "red"], ["What is 5 squared?", "25"]]),
]


def check_questions(folder, cases):
    func = function(load_student(), "load_questions")
    for number, (text, expected) in enumerate(cases):
        path = write_file(folder, "questions_%d.txt" % number, text)
        what = "load_questions on a file containing\n" + show(text) + "\n"
        result, _ = call(func, what, path)
        if not exact(as_pairs(result, what), expected):
            raise Fail(what + "should return\n" + show(expected)
                       + "\nbut returned\n" + show(result))


def case_load_questions(folder):
    check_questions(folder, QUESTION_FILES)


def case_load_questions_edges(folder):
    check_questions(folder, QUESTION_EDGES)


SAVES = [
    ("Existing,3\n", [("Ana", 4), ("Mary Ann", 8)],
     "Existing,3\nAna,4\nMary Ann,8\n"),
    ("", [("Zed", 0)], "Zed,0\n"),
]


def case_save_score(folder):
    func = function(load_student(), "save_score")
    for number, (start, saves, expected) in enumerate(SAVES):
        path = write_file(folder, "scores_%d.txt" % number, start)
        calls = []
        for name, score in saves:
            calls.append("save_score(filename, %r, %r)" % (name, score))
            result, _ = call(func, calls[-1], path, name, score)
            if result is not None:
                raise Fail(calls[-1] + " returned\n" + show(result)
                           + "\nsave_score returns nothing.")
        got = read_file(path)
        if got != expected:
            raise Fail("Starting from a file containing\n" + show(start)
                       + "\nthen calling\n" + show_lines(calls)
                       + "\nthe file should contain\n" + show(expected)
                       + "\nbut it contains\n" + show(got))


SCORE_FILES = [
    ("Alice,10\nMary Ann,8\nBo,12\n",
     [["Alice", 10], ["Mary Ann", 8], ["Bo", 12]]),
    ("Kim Lee,0\nRaj,7\nKim Lee,9\n",
     [["Kim Lee", 0], ["Raj", 7], ["Kim Lee", 9]]),
]


def case_load_scores(folder):
    func = function(load_student(), "load_scores")
    for number, (text, expected) in enumerate(SCORE_FILES):
        path = write_file(folder, "scores_%d.txt" % number, text)
        what = "load_scores on a file containing\n" + show(text) + "\n"
        result, _ = call(func, what, path)
        got = as_pairs(result, what)
        for pair in got:
            if len(pair) == 2 and type(pair[1]) is not int:
                raise Fail(what + "returned\n" + show(result) + "\nThe score "
                           + repr(pair[1]) + " is a " + type(pair[1]).__name__
                           + ", and every score must be an int.")
        if not exact(got, expected):
            raise Fail(what + "should return\n" + show(expected)
                       + "\nbut returned\n" + show(result))


BOARDS = [
    ([["Bo", 5], ["Alice", 10], ["Cy", 8], ["Dee", 5]],
     [HEADER, "1. Alice 10", "2. Cy 8", "3. Bo 5", "4. Dee 5"]),
    ([["Mary Ann", 3], ["Zoe", 12], ["Raj", 7], ["Zoe", 5]],
     [HEADER, "1. Zoe 12", "2. Raj 7", "3. Zoe 5", "4. Mary Ann 3"]),
]


def case_display(folder):
    func = function(load_student(), "display_leaderboard")
    for scores, expected in BOARDS:
        given = [list(pair) for pair in scores]
        what = "display_leaderboard(" + repr(scores) + ")"
        _, printed = call(func, what, given)
        got = output_lines(printed)
        if got != expected:
            raise Fail(what + " should print exactly\n" + show_lines(expected)
                       + "\nbut printed\n" + show_lines(got))


GAMES = [
    ("Ana", ["Paris", "56", "Mars", "Pacific", "7"]),
    ("Bo", ["Paris", "56", "Mars", "Pacific", "6"]),
]


def case_engine(folder):
    for name in ("quiz_engine.py", "questions.txt", "leaderboard.py"):
        source = os.path.join(ROOT, name)
        if not os.path.isfile(source):
            raise Fail("There is no " + name + " in your repository.")
        shutil.copy(source, os.path.join(folder, name))
    story = ("Two games were played with python3 quiz_engine.py, starting "
             "with no scores.txt: Ana answered 4 of the 5 questions "
             "correctly, then Bo answered all 5.\n")
    printed = ""
    for name, answers in GAMES:
        try:
            done = subprocess.run([sys.executable, "quiz_engine.py"],
                                  cwd=folder, capture_output=True, text=True,
                                  input="\n".join([name] + answers) + "\n",
                                  timeout=15)
        except subprocess.TimeoutExpired:
            raise Fail(story + "The game for " + name + " did not finish "
                       "within 15 seconds.")
        if done.returncode != 0:
            tail = done.stderr.strip().splitlines()[-6:]
            raise Fail(story + "The game for " + name + " crashed:\n"
                       + show_lines(tail))
        printed = done.stdout

    lines = output_lines(printed)
    if "You scored 5 out of 5" not in lines:
        raise Fail(story + "Bo's game should print the line\n"
                   "    You scored 5 out of 5\nbut it printed\n"
                   + show_lines(lines))
    board = []
    if HEADER in lines:
        last = len(lines) - 1 - lines[::-1].index(HEADER)
        board = lines[last:]
    expected = [HEADER, "1. Bo 5", "2. Ana 4"]
    if board != expected:
        raise Fail(story + "Bo's game should end with exactly\n"
                   + show_lines(expected) + "\nbut it ended with\n"
                   + show_lines(board or lines[-4:]))
    got = read_file(os.path.join(folder, "scores.txt"))
    if got != "Ana,4\nBo,5\n":
        raise Fail(story + "scores.txt should then contain\n"
                   + show("Ana,4\nBo,5\n") + "\nbut it contains\n" + show(got))


CASES = {
    "load_questions": case_load_questions,
    "load_questions_edges": case_load_questions_edges,
    "save_score": case_save_score,
    "load_scores": case_load_scores,
    "display": case_display,
    "engine": case_engine,
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in CASES:
        print("usage: python3 tests/grade_p4.py <case>, where <case> is one "
              "of: " + ", ".join(CASES))
        return 2
    folder = tempfile.mkdtemp(prefix="p4_")
    try:
        CASES[sys.argv[1]](folder)
    except Fail as err:
        print("FAIL: " + str(err))
        return 1
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
