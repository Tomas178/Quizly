from unittest import mock
from unittest import TestCase
from Enumerators.quizly_mode import QuizlyMode
from Enumerators.question_type import QuestionType
from Helpers.user_input_helper import (
    select_mode,
    question_type_selection,
    get_order_type,
    get_user_quiz_answer,
    get_user_test_length,
)
from Helpers.csv_helper import load_questions


class TestSelectMode(TestCase):
    @mock.patch("builtins.input", side_effect=["1"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.ADDING_QUESTIONS)

    @mock.patch("builtins.input", side_effect=["2"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.STATISTICS_VIEWING)

    @mock.patch("builtins.input", side_effect=["3"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.DISABLE_OR_ENABLE_QUESTIONS)

    @mock.patch("builtins.input", side_effect=["4"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.PRACTICE_MODE)

    @mock.patch("builtins.input", side_effect=["5"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.TEST_MODE)

    @mock.patch("builtins.input", side_effect=["6"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.SELECT_PROFILE)

    @mock.patch("builtins.input", side_effect=["7"])
    def test_select_mode(self, mock_input):
        self.assertEqual(select_mode(), QuizlyMode.QUIT)


class TestQuestionTypeSelection(TestCase):
    @mock.patch("builtins.input", side_effect=["1"])
    def test_question_type_selection(self, mock_input):
        self.assertEqual(question_type_selection(), QuestionType.QUIZ)

    @mock.patch("builtins.input", side_effect=["2"])
    def test_question_type_selection(self, mock_input):
        self.assertEqual(question_type_selection(), QuestionType.FREE_FORM)


class TestGetOrderType(TestCase):
    @mock.patch("builtins.input", side_effect=["ascending"])
    def test_get_order_type(self, mock_input):
        self.assertEqual(get_order_type(), "ascending")

    @mock.patch("builtins.input", side_effect=["descending"])
    def test_get_order_type(self, mock_input):
        self.assertEqual(get_order_type(), "descending")


class TestGetUserQuizAnswer(TestCase):
    @mock.patch("builtins.input", side_effect=["A"])
    def test_get_user_quiz_answer_with_A(self, mock_input):
        self.assertEqual(get_user_quiz_answer(["A", "B", "C", "D"]), "A")

    def test_get_user_quiz_answer_with_done(self):
        with mock.patch("builtins.input", side_effect=["done"]):
            self.assertEqual(get_user_quiz_answer(["A", "B", "C", "D"]), "Done")

    @mock.patch("builtins.input", side_effect=["E", "A"])
    def test_get_user_quiz_answer_with_wrong_input(self, mock_input):
        self.assertEqual(get_user_quiz_answer(["A", "B", "C", "D"]), "A")


class TestGetUserTestLength(TestCase):
    @mock.patch("builtins.input", side_effect=["5"])
    def test_get_user_test_length(self, mock_input):
        questions = load_questions()
        self.assertEqual(get_user_test_length(questions), 5)
