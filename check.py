#!/usr/bin/env python3
"""Run the same checks the autograder runs, on your own machine.

    python3 check.py

This is the whole autograder except the commit count, which only means
something once your work is pushed. If everything here says PASS, the
autograder will agree.

The function tests run tests/grade_p4.py, the same file the autograder runs,
so the two cannot drift apart.

Run it as often as you like. It never changes your code. It does write
concept_check_report.json, which git ignores.
"""
import hashlib
import os
import re
import subprocess
import sys

FILE = "leaderboard.py"
CHECKER = os.path.join("tests", "cs163_fall2026_concept_checker.py")
HARNESS = os.path.join("tests", "grade_p4.py")

# The provided files, and the SHA-256 of each as provided (line endings
# ignored). The autograder checks these before every test, and if any one has
# changed, every test scores 0.
PROVIDED = {
    "quiz_engine.py":
        "a12b9d10c5ff48aaff6b279a6368397ee9ec19efee45f64767f6c1bf40b37d1f",
    "questions.txt":
        "8cf2f8d96b8e3f8b78f29dcc51f95edf9afd5a322d8366640d1f3ebd962f9ef9",
    "tests/grade_p4.py":
        "0a2f3ad7dedd693520825a43cc0ce397e48c3966d9a226975d79e13a5c2e0090",
    "tests/cs163_fall2026_concept_checker.py":
        "fb52b5b62ed0c335190b207155749131844268b4a1abce0d8476ad4ef3045825",
}

# Name, points, and the harness case the autograder runs for that test.
TESTS = [
    ("Load questions", 6, "load_questions"),
    ("Load questions edge cases", 4, "load_questions_edges"),
    ("Save score appends", 5, "save_score"),
    ("Load scores", 5, "load_scores"),
    ("Leaderboard display", 6, "display"),
    ("Plays through the engine", 5, "engine"),
]


def changed_provided_files():
    changed = []
    for name, expected in PROVIDED.items():
        try:
            with open(name, "rb") as handle:
                data = handle.read().replace(b"\r", b"")
        except OSError:
            changed.append(name)
            continue
        if hashlib.sha256(data).hexdigest() != expected:
            changed.append(name)
    return changed


def run_case(case):
    # Same rule as the autograder: exit status 0 and a last line of PASS.
    try:
        done = subprocess.run([sys.executable, "-I", HARNESS, case],
                              stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "your code did not finish within 60 seconds"
    lines = [x for x in done.stdout.splitlines() if x.strip()]
    if done.returncode == 0 and lines and lines[-1] == "PASS":
        return True, ""
    detail = (done.stdout + done.stderr).strip()
    if not detail:
        detail = "the test ended before it could print PASS"
    if detail.startswith("FAIL: "):
        detail = detail[len("FAIL: "):]
    return False, detail


def main():
    if not os.path.exists(FILE):
        print("There is no " + FILE + " in this folder. Are you in your repo?")
        return 1

    earned = 0
    possible = 0
    failures = []

    print("=" * 64)
    print("  Project 4 self-check")
    print("=" * 64)

    changed = changed_provided_files()
    if changed:
        print("  FAIL   Provided files are unchanged (every test)")
        for name in changed:
            failures.append(
                name + " is not the file you were given. The autograder "
                "scores every test 0 until it is put back. To restore it, "
                "run: git checkout $(git rev-list --max-parents=0 HEAD) -- "
                + name)

    possible += 3
    # Must match the autograder, which greps the whole file:
    #     grep -qE "^# Name:[[:space:]]*[^[:space:]]" leaderboard.py
    # utf-8-sig drops a byte order mark, which the autograder also allows.
    with open(FILE, "r", encoding="utf-8-sig", errors="replace") as handle:
        source = handle.read()
    if re.search(r"^# Name:[^\S\r\n]*\S", source, re.MULTILINE):
        earned += 3
        print("  PASS   File header (3)")
    else:
        print("  FAIL   File header (3)")
        failures.append("Fill in your name on the first line, after '# Name:'")

    possible += 4
    result = subprocess.run([sys.executable, "-I", CHECKER, "--project", "4",
                             "--strict", FILE], capture_output=True, text=True)
    if result.returncode == 0:
        earned += 4
        print("  PASS   Concept check (4)")
    else:
        print("  FAIL   Concept check (4)")
        for text in result.stdout.splitlines():
            stripped = text.strip()
            if stripped.startswith("your program does not contain"):
                failures.append(stripped[0].upper() + stripped[1:])
            elif stripped.startswith(FILE + ":"):
                failures.append("Not allowed here: " + stripped)

    for name, points, case in TESTS:
        possible += points
        passed, detail = run_case(case)
        if passed:
            earned += points
            print("  PASS   %s (%d)" % (name, points))
        else:
            print("  FAIL   %s (%d)" % (name, points))
            failures.append(name + ": " + detail)

    if changed:
        earned = 0
    print("-" * 64)
    print("  %d of %d points from the checks that run locally"
          % (earned, possible))
    if not changed:
        print("  Plus 2 points for committing at least 3 times as you work.")
    print("=" * 64)

    if failures:
        print("\nWhat to fix:\n")
        for item in failures:
            print("  - " + item.replace("\n", "\n    "))
        print()
        return 1

    print("\nEverything passes. Commit, push, and submit your repo URL "
          "in Canvas.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
