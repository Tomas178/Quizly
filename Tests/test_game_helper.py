from unittest import mock
from Models.question import Question
from Helpers.game_helper import start_free_form, is_user_answer_correct
from Helpers.csv_helper import load_profile_with_statistics


def test_start_free_form():
    with mock.patch("builtins.input", side_effect=["Paris"]):
        assert start_free_form() == "Paris"


def test_is_user_answer_correct():
    question = Question(
        1,
        "What is the capital of France?",
        "Paris",
        True,
    )
    profile = load_profile_with_statistics("default")
    assert is_user_answer_correct("Paris", "Paris", profile, question) == True
    assert is_user_answer_correct("London", "Paris", profile, question) == False
