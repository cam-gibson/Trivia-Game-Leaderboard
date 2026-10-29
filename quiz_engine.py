# quiz_engine.py
# PROVIDED FILE - DO NOT MODIFY
#
# This is the trivia game engine. It calls the four functions you write in
# leaderboard.py. You do not need to read or understand every line, but you
# may read it to see exactly how and when your functions are called.

from leaderboard import (
    load_questions,
    save_score,
    load_scores,
    display_leaderboard,
)

QUESTIONS_FILE = "questions.txt"
SCORES_FILE = "scores.txt"


def ensure_scores_file_exists():
    """Create the scores file if it does not already exist."""
    with open(SCORES_FILE, "a"):
        pass


def play_game(player_name):
    """Run one trivia game for the given player and return their score."""
    questions = load_questions(QUESTIONS_FILE)
    if not questions:
        print("No questions available.")
        return 0

    score = 0
    for pair in questions:
        question = pair[0]
        answer = pair[1]
        print(question)
        guess = input("Your answer: ")
        if guess.strip().lower() == answer.strip().lower():
            print("Correct!")
            score = score + 1
        else:
            print("Incorrect. The answer was: " + answer)

    print("You scored " + str(score) + " out of " + str(len(questions)))
    return score


def main():
    """Entry point: play a game, save the score, show the leaderboard."""
    ensure_scores_file_exists()
    player_name = input("Enter your name: ")
    score = play_game(player_name)
    save_score(SCORES_FILE, player_name, score)
    scores = load_scores(SCORES_FILE)
    display_leaderboard(scores)


if __name__ == "__main__":
    main()
