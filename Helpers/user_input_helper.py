from Enumerators.quizly_mode import QuizlyMode
from Models.question import Question


def select_mode() -> QuizlyMode:
    for mode in QuizlyMode:
        print(f"{mode.value}. {' '.join(mode.name.split('_')).capitalize()}")

    selected_mode = None
    while selected_mode == None:
        try:
            user_input = int(input("Enter a number: "))
            selected_mode = QuizlyMode(user_input)
        except ValueError:
            print("Please enter a number.")
            continue
    print(f"\nSelected mode: {' '.join(selected_mode.name.split('_')).capitalize()}\n")
    return selected_mode


def question_type_selection() -> int:
    print("1. Quiz questions\n2. Free-form text questions.")
    while True:
        user_input = input("Enter a number: ")
        if user_input not in ["1", "2"]:
            print("Please enter 1 or 2.")
            continue

        return int(user_input)


def get_order_type() -> str:
    while True:
        order = (
            input("Sort questions by score 'ascending' or 'descending'?: ")
            .lower()
            .strip()
        )
        if order not in ["ascending", "descending"]:
            print("Invalid ordering type! Please enter: 'ascending' or 'descending'.")
            continue
        break
    return order


def get_user_test_answer(choices: list[str]) -> str:
    while True:
        user_answer = input("Enter your answer: ").strip().capitalize()
        if user_answer == "Done":
            return user_answer
        elif user_answer not in choices:
            print("Invalid choice! Please try again.")
            continue
        return user_answer


def get_user_test_length(questions: list[Question]) -> int:
    enabled_questions_count = 0
    for question in questions:
        enabled_questions_count += 1 if question.is_enabled else 0
    while True:
        try:
            user_input = int(
                input(
                    f"Enter the number of questions to test [1-{enabled_questions_count}]: "
                )
            )
            if user_input < 1 or user_input > enabled_questions_count:
                print("Invalid number! Please try again.")
                continue
            return user_input
        except ValueError:
            print("Please enter a number!")
            continue


def select_profile() -> str:
    print("Would you like to select or create a new profile?")
    while True:
        user_input = input("Enter 'select' or 'create': ").lower().strip()
        if user_input not in ["select", "create"]:
            print("Invalid choice! Please enter 'select' or 'create'.")
            continue
        return user_input


def check_new_profile_name_validity(profile_name: str) -> bool:
    if not profile_name:
        print("Profile name cannot be empty!")
        return False
    elif profile_name.isdecimal():
        print("Profile name cannot be a number! Please try again.")
        return False
    return True


def add_another_question() -> bool:
    while True:
        decision = (
            input("\nWould you like to add another question? [y/n]: ").strip().lower()
        )

        if decision == "y":
            return True
        elif decision == "n":
            return False
        else:
            print("Please enter 'y' or 'n'.")
            continue
