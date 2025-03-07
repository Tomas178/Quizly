import sys
import random
from tabulate import tabulate
from Enumerators.quizly_mode import QuizlyMode
from Enumerators.question_type import QuestionType
from Helpers import user_input_helper, csv_helper, question_helper, game_helper
from Models.question import Question
from Models.profile import Profile

MINIMUM_CHOICES_REQUIRED = 2
MAXIMUM_CHOICES_ALLOWED = 4


def main():
    questions = csv_helper.load_questions()
    profile = csv_helper.load_profile_with_statistics("default")
    profile.init_statistics(questions)
    while True:
        print(f"Current profile: {profile.name}")
        try:
            mode = user_input_helper.select_mode()
            match mode:
                case QuizlyMode.ADDING_QUESTIONS:
                    add_questions(questions)
                    profile.init_statistics(questions)
                case QuizlyMode.STATISTICS_VIEWING:
                    view_statistics(questions, profile)
                case QuizlyMode.DISABLE_OR_ENABLE_QUESTIONS:
                    disable_or_enable_questions(questions)
                case QuizlyMode.PRACTICE_MODE:
                    practice_mode(questions, profile)
                case QuizlyMode.TEST_MODE:
                    test_mode(questions, profile)
                case QuizlyMode.PROFILE_SELECT:
                    profile = select_profile(profile)
                    profile.init_statistics(questions)
                case QuizlyMode.QUIT:
                    print("\nSaving...")
                    csv_helper.save_questions(questions)
                    csv_helper.save_question_statistics(profile)
                    sys.exit("\nThanks for playing!")
        except KeyboardInterrupt:
            print("\nSaving...")
            csv_helper.save_questions(questions)
            csv_helper.save_question_statistics(profile)
            sys.exit("\nThanks for playing!")


def add_questions(questions: list[Question]) -> None:
    """Allows the user to add questions to the list of questions."""

    print("Please enter following details to complete question addition.\n")

    previous_count = len(questions)
    questions_highest_id = csv_helper.find_questions_max_id() + 1

    while True:
        try:
            print(f"Adding question {questions_highest_id}")
            question_type = user_input_helper.question_type_selection()
            if question_type == QuestionType.QUIZ:
                title = input("Question: ").strip().capitalize()
                answer = input("Answer: ").strip()
                print("Answer is automatically added to the choices list!")
                choices = [answer]
                while len(choices) != MAXIMUM_CHOICES_ALLOWED:
                    choice = input(
                        f"Choice {len(choices) + 1} (Leave empty and press 'Enter' to stop entering): "
                    ).strip()

                    if choice == "":
                        if (
                            len(choices) >= MINIMUM_CHOICES_REQUIRED
                            and len(choices) <= MAXIMUM_CHOICES_ALLOWED
                        ):
                            break
                        else:
                            print(
                                f"Add atleast {MINIMUM_CHOICES_REQUIRED - len(choices)} more choices!"
                            )
                            continue
                    # +1 because we check if after the addition of the choice we have 4 choices
                    elif len(choices) + 1 == MAXIMUM_CHOICES_ALLOWED:
                        choices.append(choice)
                        print("You have entered maximum amount of choices allowed")
                        break
                    else:
                        choices.append(choice)

                if not title or not answer:
                    print("Title or Answer cannot be empty! Please try again")
                    continue
                else:
                    questions.append(
                        Question(questions_highest_id, title, answer, choices=choices)
                    )
            elif question_type == QuestionType.FREE_FORM:
                title = input("Question: ").strip().capitalize()
                answer = input("Answer: ").strip()

                if not title or not answer:
                    print("Title or Answer cannot be empty! Please try again")
                    continue
                else:
                    questions.append(Question(questions_highest_id, title, answer))

            questions_highest_id += 1

            if not user_input_helper.add_another_question():
                print(
                    f"\nExiting. Successfully added {len(questions) - previous_count} new questions!\n"
                )
                return questions
            else:
                print()

        except KeyboardInterrupt:
            print(
                f"Exiting. Successfully added {len(questions) - previous_count} new questions!"
            )
            return questions


def view_statistics(questions: list[Question], profile: Profile) -> None:
    """Prints out the statistics for each question in the list of questions in user selected order."""

    print("\nWelcome to Statistics View!")

    if len(questions) == 0:
        print("Unable to view statistics if no questions are found!\n")
        return

    order = user_input_helper.get_order_type()

    print(f"Displaying statistics for '{profile.name}' profile...")

    data = question_helper.get_statistics_for_questions(questions, profile)

    reverse_order = order == "descending"
    # Using lambda, sort by score
    data.sort(key=lambda x: x[4], reverse=reverse_order)

    columns = ["Question ID", "Title", "Answer", "is_enabled", "Score (%)"]
    print(tabulate(data, headers=columns, tablefmt="grid"))
    print()


def disable_or_enable_questions(questions: list[Question]) -> None:
    """Allows the user to disable or enable questions in the list of questions."""

    if len(questions) == 0:
        print("Unable to disable/enable questions, because there are no questions")
        return questions

    data = [[q.id, q.title, q.answer, q.is_enabled] for q in questions]
    columns = ["id", "title", "answer", "is_enabled"]
    print(tabulate(data, headers=columns, tablefmt="grid"))

    print("\nSelect the ID of a question to disable/enable.")
    while True:
        try:
            question_id = int(input("Question ID: "))
        except ValueError:
            print("Please enter a number!")
            continue

        index = -1
        for i, q in enumerate(questions):
            if q.id == question_id:
                q.is_enabled = not q.is_enabled
                index = i
                break

        if index == -1:
            print("Invalid ID!. Enter again.")
            continue

        print(f"\nSuccessfully changed question {question_id} is_enabled status!\n")
        print(tabulate([data[index]], headers=columns, tablefmt="grid"))
        print()
        return


def practice_mode(questions: list[Question], profile: Profile) -> None:
    """Starts practice mode where the user can practice answering questions until 'done' is entered."""

    print("\nWelcome to Practice Mode!")
    if not question_helper.is_enough_questions(questions, "Practice"):
        return
    elif not question_helper.is_enough_enabled_questions(questions, "Practice"):
        return

    while True:
        print("When you want to end Practice Mode enter 'done'")

        question = question_helper.get_random_questions(questions, profile)[0]
        correct_answer = question.answer
        print(f"Question: {question.title}")

        if Question.is_quiz(question):
            user_answer = game_helper.start_quiz(question)
            if user_answer == "Done":
                print("Exiting Practice Mode...")
                break
        else:
            user_answer = game_helper.start_free_form()

            if user_answer == "Done":
                print("Exiting Practice Mode...")
                break

        game_helper.check_answer(user_answer, correct_answer, profile, question)


def test_mode(questions: list[Question], profile: Profile) -> None:
    """
    Starts test mode where the user can take a test with a selected number of questions. Also 'done' can be written to end the test.
    """

    print("\nWelcome to Test Mode!")
    if not question_helper.is_enough_questions(questions, "Test"):
        return
    elif not question_helper.is_enough_enabled_questions(questions, "Test"):
        return

    test_length = user_input_helper.get_user_test_length(questions)
    test_questions = question_helper.get_test_questions(questions, test_length)
    correct_answers = 0

    for question in test_questions:
        print("When you want to end Test Mode enter 'done'")

        correct_answer = question.answer
        print(f"Question: {question.title}")

        if question.is_quiz():
            user_answer = game_helper.start_quiz(question)
            if user_answer == "Done":
                print("Exiting Test Mode...")
                break
        else:
            user_answer = game_helper.start_free_form()

            if user_answer == "Done":
                print("Exiting Test Mode...")
                break

        if game_helper.is_user_answer_correct(
            user_answer, correct_answer, profile, question
        ):
            correct_answers += 1

    game_helper.print_test_results(test_length, correct_answers)
    csv_helper.export_test_result(test_length, correct_answers, profile)


def select_profile(profile: Profile) -> Profile:
    """Allows the user to select an already existing profile or create a new one."""

    user_choice = user_input_helper.select_profile()

    if profile and profile.question_statistics:
        print("Saving current profile question statistics...\n")
        csv_helper.save_question_statistics(profile)

    if user_choice == "select":
        print("Loading available profiles...")
        profiles = csv_helper.load_profile_names()

        if len(profiles) <= 1:
            print("Please create more profiles before selecting\n")
            return profile

        profiles_data = [[profile.id, profile.name] for profile in profiles]
        columns = ["Profile ID", "Name"]
        print(tabulate(profiles_data, columns, tablefmt="grid"))

        print("\nPlease type the ID of the profile you would like to select.")
        while True:
            try:
                profile_id = int(input("Profile ID: "))
            except ValueError:
                print("Please enter a number!")
                continue

            new_profile = None
            for profile in profiles:
                if profile.id == profile_id:
                    new_profile = csv_helper.load_profile_statistics(
                        Profile(profile.id, profile.name, None)
                    )
                    break

            if not new_profile:
                print("Invalid ID!. Enter again.")
                continue

            print(f"You successfully selected profile: {profile.name.title()}!\n")
            return new_profile
    else:
        profile_id = csv_helper.find_profile_max_id()
        while True:
            new_profile_name = input("Enter a name for the new profile: ").strip()
            if not user_input_helper.check_new_profile_name_validity(new_profile_name):
                continue
            new_profile = Profile(profile_id + 1, new_profile_name, None)
            if not csv_helper.create_new_profile(new_profile):
                print("Profile name already exists! Please try again.")
                continue
            else:
                print(
                    f"Successfully created a new profile {new_profile_name.title()}!\n"
                )
                return new_profile


if __name__ == "__main__":
    main()


# https://github.com/Tomas178/War-game
