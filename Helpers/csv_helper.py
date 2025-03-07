import csv
import os
from datetime import datetime
from Models.question import Question
from Models.profile import Profile
from Models.question_statistics import QuestionStatistics

QUESTIONS_FILE_PATH = "Data/questions.csv"
QUESTIONS_STATISTICS_FILE_PATH = "Data/questions_statistics.csv"
PROFILES_FILE_PATH = "Data/profiles.csv"
RESULTS_FILE_PATH = "Data/results.txt"


def validate_file(file_path: str, required_headers: list[str]) -> bool:
    """Validates the file at the given path and creates it if it does not exist."""

    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_exists = os.path.exists(file_path)
    if file_exists:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            first_row = next(reader, None)

            if first_row == required_headers:
                return True

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(required_headers)

        return False


def load_questions() -> list[Question]:
    """Loads questions from the questions file."""

    headers = ["id", "title", "answer", "is_enabled", "choices"]

    if not validate_file(QUESTIONS_FILE_PATH, headers):
        return []

    questions = []
    with open(QUESTIONS_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                choices = row["choices"].split("|") if row["choices"] else []
                questions.append(
                    Question(
                        id=int(row["id"]),
                        title=row["title"],
                        answer=row["answer"],
                        is_enabled=row["is_enabled"] == "True",
                        choices=choices,
                    )
                )
            except ValueError:
                print(f"Invalid id found: {row[0]}. Skipping question.")
            except IndexError:
                print(f"Skipping incomplete line: {row}.")

    return questions


def save_questions(questions: list[Question]) -> None:
    """Saves the questions to the questions file."""

    headers = ["id", "title", "answer", "is_enabled", "choices"]

    with open(QUESTIONS_FILE_PATH, "w", newline="") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(question.to_dict() for question in questions)

    print("Successfully saved questions!")


def load_profile_with_statistics(profile_name: str) -> Profile:
    """Loads a profile with statistics from the profiles file."""

    headers = ["id", "name"]
    default_profile = Profile("0", "default", {})
    # If profile file has not been created or is invalid, correct it and return a default profile
    if not validate_file(PROFILES_FILE_PATH, headers):
        create_new_profile(default_profile)
        return default_profile

    profile_id = None
    with open(PROFILES_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                if line["name"] == profile_name:
                    profile_id = int(line["id"])
                    break
            except ValueError:
                print(f"Failed to convert data for profile line: {line}")
            except KeyError:
                print(f"Missing data in line: {line}")

    # If profile was not found, return default profile
    if profile_id == None:
        return default_profile

    return load_profile_statistics(Profile(profile_id, profile_name, {}))


def create_new_profile(profile: Profile) -> bool:
    """Creates a new profile in the profiles file."""

    headers = ["id", "name"]

    validate_file(PROFILES_FILE_PATH, headers)

    with open(PROFILES_FILE_PATH) as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line["name"] == profile.name:
                return False

    with open(PROFILES_FILE_PATH, "a", newline="") as file:
        writer = csv.DictWriter(file, headers)
        new_profile = {"id": profile.id, "name": profile.name}
        writer.writerow(new_profile)

    return True


def load_profile_with_statistics(profile_name: str) -> Profile:
    """Loads a profile with statistics from the profiles file."""

    headers = ["id", "name"]
    default_profile = Profile("0", "default", {})
    # If profile file has not been created or is invalid, correct it and return a default profile
    if not validate_file(PROFILES_FILE_PATH, headers):
        create_new_profile(default_profile)
        return default_profile

    profile_id = None
    with open(PROFILES_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                if line["name"] == profile_name:
                    profile_id = int(line["id"])
                    break
            except ValueError:
                print(f"Failed to convert data for profile line: {line}")
            except KeyError:
                print(f"Missing data in line: {line}")

    # If profile was not found, return default profile
    if profile_id == None:
        return default_profile

    return load_profile_statistics(Profile(profile_id, profile_name, {}))


def load_profile_statistics(profile: Profile) -> Profile:
    """Loads the question statistics for a profile."""

    headers = [
        "profile_id",
        "question_id",
        "times_answered",
        "times_answered_correctly",
        "weight",
    ]

    if not validate_file(QUESTIONS_STATISTICS_FILE_PATH, headers):
        return Profile(profile.id, profile.name, {})

    question_statistics = {}
    with open(QUESTIONS_STATISTICS_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                if int(line["profile_id"]) == profile.id:
                    question_id = int(line["question_id"])
                    question_statistics[question_id] = QuestionStatistics(
                        times_answered=int(line["times_answered"]),
                        times_answered_correctly=int(line["times_answered_correctly"]),
                        weight=float(line["weight"]),
                    )
            except ValueError:
                print(f"Failed to convert data for question statistics line: {line}")
            except KeyError:
                print(f"Missing data in line: {line}")

    return Profile(profile.id, profile.name, question_statistics)


def save_question_statistics(profile: Profile) -> None:
    """Saves the question statistics for a profile."""

    if not profile.question_statistics:
        return

    headers = [
        "profile_id",
        "question_id",
        "times_answered",
        "times_answered_correctly",
        "weight",
    ]

    validate_file(QUESTIONS_STATISTICS_FILE_PATH, headers)

    existing_data = []
    with open(QUESTIONS_STATISTICS_FILE_PATH) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["profile_id"]) != profile.id:
                existing_data.append(
                    {
                        "profile_id": row["profile_id"],
                        "question_id": row["question_id"],
                        "times_answered": row["times_answered"],
                        "times_answered_correctly": row["times_answered_correctly"],
                        "weight": row["weight"],
                    }
                )

    rows = [
        statistics.to_dict(profile.id, question_id)
        for question_id, statistics in profile.question_statistics.items()
    ]

    rows.extend(existing_data)

    with open(QUESTIONS_STATISTICS_FILE_PATH, "w", newline="") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(rows)

    print("Successfully saved question statistics!")


# Loads all profile names from file
def load_profile_names() -> list[Profile]:
    """Loads all profile names from the profiles file."""

    profiles = []
    with open(PROFILES_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            profiles.append(Profile(int(line["id"]), line["name"], {}))

    return profiles


def export_test_result(
    test_length: int, correct_answers: int, profile: Profile
) -> None:
    """Exports the test results to the results file."""

    score = round(correct_answers / test_length * 100, 1)
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("Data/results.txt", "a") as file:
        file.write(
            f"{profile.name} got {correct_answers} out of {test_length} ({score}%). Completion time: {completion_time}\n"
        )
    print("Successfully exported test result to Data/results.txt!")


def find_max_id(id_column_name: str, file_path: str) -> int:
    """Finds the maximum id in the file."""

    max_id = -1
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for line in reader:
            try:
                max_id = max(max_id, int(line[id_column_name]))
            except ValueError as e:
                print(f"Invalid column name provided or corrupt file data: {e}")
                continue

    return max_id


def find_profile_max_id() -> int:
    """Finds the maximum profile id in the profiles file."""
    return find_max_id("id", PROFILES_FILE_PATH)


def find_questions_max_id() -> int:
    """Finds the maximum question id in the questions file."""
    return find_max_id("id", QUESTIONS_FILE_PATH)
