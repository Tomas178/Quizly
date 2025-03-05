import random
from Models.question import Question
from Models.profile import Profile
from Helpers import user_input_helper

AVAILABLE_QUIZ_LETTERS = ["A", "B", "C", "D"]


def start_quiz(question: Question) -> str:
    print("Choices:")
    choices = question.choices.copy()
    random.shuffle(choices)
    for i, choice in enumerate(choices):
        print(f"{AVAILABLE_QUIZ_LETTERS[i]}. {choice}")

    user_answer = user_input_helper.get_user_test_answer(AVAILABLE_QUIZ_LETTERS)

    if user_answer == "Done":
        return user_answer

    return choices["ABCD".index(user_answer)]


def start_free_form() -> str:
    return input("Enter your answer: ").strip()


def is_user_answer_correct(
    user_answer: str, correct_answer: str, profile: Profile, question: Question
) -> bool:
    if user_answer == correct_answer:
        print("\nCorrect!\n")
        profile.get_statistics_for_question(question.id).update_statistics(True)
        return True
    elif user_answer != correct_answer:
        print("\nIncorrect!\n")
        profile.get_statistics_for_question(question.id).update_statistics(False)
        return False


def print_test_results(test_length, correct_answers) -> None:
    score = round(correct_answers / test_length * 100, 1)
    print("Test finished!")
    print(f"Your score: {score}%")
