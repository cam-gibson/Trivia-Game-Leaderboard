# Name: Cameron Gibson
# Date: 10/29/26
# Description:

def load_questions(filename):
    """Returns questions and answers."""
    questions = []

    with open(filename, "r") as file:
        for line in file:
            question = line.rstrip("\r\n")
            answer = file.readline()

            if answer != "":
                questions.append([question, answer.rstrip("\r\n")])

    return questions


def save_score(filename, name, score):
    """Save the player's name and score."""
    with open(filename, "a+") as file:
        file.seek(0)
        contents = file.read()

        if contents != "" and not contents.endswith("\n"):
            file.write("\n")

        file.write(f"{name},{score}\n")


def load_scores(filename):
    """Load the saved names and scores."""
    scores = []

    with open(filename, "r") as file:
        for line in file:
            parts = line.rstrip("\r\n").split(",")
            name = parts[0]
            score = int(parts[1])
            scores.append([name, score])

    return scores



def display_leaderboard(scores):
    """Show the scores from highest to lowest."""
    def get_score(entry):
        return entry[1]

    ranked_scores = sorted(scores, key = get_score, reverse = True)

    print("=== Leaderboard ===")

    position = 1

    for entry in ranked_scores:
        print(f"{position}. {entry[0]} {entry[1]}")
        position += 1