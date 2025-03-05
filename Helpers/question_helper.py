from Models.question import Question
from Models.profile import Profile
import random


def get_random_questions(
    questions: list[Question], profile: Profile, k: int = 1
) -> Question:
    weighted_questions = []
    weights = []
    for question in questions:
        if not question.is_enabled:
            continue
        stats = profile.get_statistics_for_question(question.id)
        weight = stats.weight if stats else 1.0
        weighted_questions.append(question)
        weights.append(weight)

    return random.choices(weighted_questions, weights, k=k)


def is_enough_questions(questions: list[Question], mode: str) -> bool:
    if len(questions) < 5:
        print(f"Add {5 - len(questions)} more questions to begin the {mode}.")
        return False
    else:
        return True


def is_enough_enabled_questions(questions: list[Question], mode: str) -> bool:
    enabled_questions_count = 0
    for question in questions:
        enabled_questions_count += 1 if question.is_enabled else 0

    if enabled_questions_count < 5:
        print(
            f"Enable {5 - enabled_questions_count} more questions to begin the {mode}."
        )
        return False
    else:
        return True


def get_enabled_questions(questions: list[Question]) -> list[Question]:
    enabled_questions = []
    for question in questions:
        if question.is_enabled:
            enabled_questions.append(question)

    return enabled_questions


def get_statistics_for_questions(questions: list[Question], profile: Profile) -> list:
    data = []
    for question in questions:
        stat = profile.get_statistics_for_question(question.id)
        if stat.times_answered != 0:
            score = round(stat.times_answered_correctly / stat.times_answered * 100)
        else:
            score = 0
        data.append(
            [question.id, question.title, question.answer, question.is_enabled, score]
        )

    return data
