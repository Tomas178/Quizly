from unittest import TestCase
from Helpers.question_helper import is_enough_questions, is_enough_enabled_questions
from Helpers.csv_helper import load_questions

MODE = "practice"


class TestIsEnoughQuestions(TestCase):
    def test_is_enough_questions_from_file(self):
        questions = load_questions()
        self.assertEqual(is_enough_questions(questions, MODE), True)

    def test_is_enough_questions_empty(self):
        questions = []
        self.assertEqual(is_enough_questions(questions, MODE), False)

    def test_is_enough_questions_less_than_5(self):
        questions = load_questions()[:4]
        self.assertEqual(is_enough_questions(questions, MODE), False)


class TestIsEnoughEnabledQuestions(TestCase):
    def test_is_enough_enabled_questions_from_file(self):
        questions = load_questions()
        self.assertEqual(is_enough_questions(questions, MODE), True)

    def test_is_enough_enabled_questions_empty(self):
        questions = []
        self.assertEqual(is_enough_questions(questions, MODE), False)

    def test_is_enough_enabled_questions_less_than_5(self):
        questions = load_questions()
        enabled_questions = []
        enabled_questions_count = 0
        for question in questions:
            if enabled_questions_count == 5:
                break
            elif question.is_enabled:
                enabled_questions.append(question)
                enabled_questions_count += 1

        enabled_questions[0].is_enabled = False

        self.assertEqual(is_enough_enabled_questions(enabled_questions, MODE), False)
