# COMP 163 - Project 4: Trivia Game Leaderboard

**Chapters 7 and 8: Functions and Files**

A trivia game engine is provided in `quiz_engine.py`. It asks the questions and
keeps score. You write the four functions it calls to load the questions, save
a score, load the scores and show the leaderboard.

> **If anything here disagrees with the instructions on Canvas, Canvas is
> correct.** This file exists so the exact requirements sit next to your code.
> Canvas has the full assignment description, the grading breakdown, the due
> date, and any updates posted after the project was released.

Your file is `leaderboard.py`.

## The files

| File | What it is |
|---|---|
| `leaderboard.py` | Yours. All four functions go here. |
| `quiz_engine.py` | The game. Run it with `python3 quiz_engine.py`. |
| `questions.txt` | The questions the game asks. |
| `check.py` | Runs the autograder's checks on your machine. |
| `tests/` | The autograder's own files. |

Do not change `quiz_engine.py`, `questions.txt`, or anything in `tests/`. The
autograder checks that they are exactly as provided before it runs any test,
and if one has changed, every test scores 0. `check.py` tells you if this has
happened and how to put the file back.

Read `quiz_engine.py`. It shows when each of your functions is called and what
the game does with the result.

## The file formats

**Questions file.** Two lines per question: the question, then its answer.

```
What is the capital of France?
Paris
What is 7 times 8?
56
```

**Scores file.** One entry per line, the name, a comma, and the score, with no
spaces around the comma. Names may contain spaces but never a comma.

```
Alice,8
Mary Ann,5
```

The test files never contain blank lines, and no line starts or ends with a
space.

## The four functions

The engine imports these by name, so the names and parameters must match
exactly.

### `load_questions(filename)`

Reads a questions file and returns a list of `[question, answer]` pairs, in the
order they appear in the file. Neither string includes a line ending.

- An empty file returns `[]`.
- If the file has an odd number of lines, the last line has no answer and is
  ignored.
- The last line of the file may or may not end with a newline. Both must work.

### `save_score(filename, name, score)`

Adds one line to the end of the scores file: the name, a comma, the score, and
a newline. It never removes or changes what is already there. It returns
nothing.

Saving `Ana` with 4 and then `Mary Ann` with 8 onto a file that holds
`Existing,3` leaves this:

```
Existing,3
Ana,4
Mary Ann,8
```

### `load_scores(filename)`

Reads the scores file and returns a list of `[name, score]` pairs, in the order
they appear in the file. Each score is an `int`.

### `display_leaderboard(scores)`

Receives a list of `[name, score]` pairs, such as the one `load_scores`
returns, and prints the leaderboard. It prints exactly these lines and nothing
else:

```
=== Leaderboard ===
1. Alice 10
2. Mary Ann 8
3. Bo 8
```

- Highest score first.
- Equal scores keep the order they had in the list you were given.
- Positions count 1, 2, 3 and so on, even when scores are tied.
- One space after the period, and one space between the name and the score.
- One line per pair, so a name that appears twice is listed twice.

## Rules

- **Only function definitions at the top level.** Apart from your header
  comment, everything in `leaderboard.py` sits inside a `def`. The autograder
  imports your file, and any other line at the top level runs the moment it
  does. That includes test calls and `if __name__ == "__main__":`. Test your
  functions with `python3 quiz_engine.py` and `python3 check.py`.
- **Each of the four functions has a docstring.** Section 7.16 shows what one
  is.
- **Every `open()` is inside a `with` statement.** Section 8.6 covers `with`.
  An `open()` anywhere else fails the concept check, even if you close the file
  yourself.

## What you may use

**This project covers Chapters 7 and 8.**

You may use anything from Chapters 1 through 8, including functions you define
yourself, lists, tuples, dictionaries, string methods, and reading and writing
files.

These are not allowed:

| Not allowed here | Why |
|---|---|
| `lambda` | Not taught in this course |
| Classes | Chapter 9 |
| `try` / `except` and `raise` | Chapter 11 |
| `import` of anything, `__import__()`, `exec()`, `eval()` | Not allowed in projects. The engine does the importing |
| `exit()` and `quit()` | Not allowed in projects |
| `compile()`, `breakpoint()` and `help()` | Not allowed in projects |
| `getattr()`, `setattr()`, `delattr()`, `vars()`, `globals()` and `locals()` | Not allowed in projects |
| Names that start and end with two underscores, such as `__builtins__` or `__class__`, other than `__name__` | Not allowed in projects |
| Comprehensions, generator expressions and `match` | Not taught in this course |
| `yield`, `async` and `await` | Not taught in this course |

The autograder checks this on every push, and the check is worth 4 points, so
using any of these costs you those 4 straight away. That is not the whole cost.
A confirmed use of anything in this table is a zero on the project once I
review it.

## AI

No AI on this project, with one exception. You may use it as a rubber duck:
explain your problem to it, and take a hint from it once you have struggled
long enough to have earned one. It does not write your code.

## Check your work before you push

```
python3 check.py
```

This runs every check the autograder runs, except the commit count, and tells
you what went wrong in any test that fails. If `check.py` is clean, the
autograder will be too.

`python3 quiz_engine.py` plays the game with your functions. It adds your
score to `scores.txt`, which stays on your machine and is never pushed.

## Grading

This repository is worth 40 points. The Project 4 Tech Interview is a separate
60-point grade, for 100 in total.

| Component | Points |
|---|---|
| File header filled in | 3 |
| At least 3 commits | 2 |
| Concept check (required and forbidden features) | 4 |
| Load questions | 6 |
| Load questions edge cases | 4 |
| Save score appends | 5 |
| Load scores | 5 |
| Leaderboard display | 6 |
| Plays through the engine | 5 |
| **Total** | **40** |

### About the header

The first lines of `leaderboard.py` must be filled in:

```
# Name: Your Name
# Date: 2026-10-19
# Description: A short description of your program
```

The file ships with those labels blank. Blank scores nothing.

### About the commits

You get 2 points for making at least three commits. A commit is a save point.
When you break something at 11pm, the last commit that worked is how you get
back without starting over.

Commit when you finish a piece, not all at once at the end:

```
git add leaderboard.py
git commit -m "load_questions reads the question file"
git push
```

## Submitting

Due **Friday, October 30, 2026 at 11:59 PM**. Two steps, and you need both:

1. **Push to this repository.** Every push runs the checks automatically, and
   the most recent push before the deadline is what gets graded.
2. **Paste this repository's URL into the Canvas assignment.**

The URL by itself grades nothing. It tells me which repository is yours. It
looks something like:

```
https://github.com/COMP-163/fall-2026-comp163-project-4-yourusername
```

Copy it out of your browser's address bar rather than typing it.
