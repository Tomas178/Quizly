# Quizly

## Main functions for user

<details>

<summary><strong>1. Adding questions.</strong></summary>

```python
def add_questions(questions: list[Question]) -> None:
```

1. User is allowed to choose between quiz and free-form types:
```python 
question_type = user_input_helper.question_type_selection()
```
2. User is allowed to add more questions without returning to the main menu:
```python 
if not user_input_helper.add_another_question():
    print(
        f"\nExiting. Successfully added {len(questions) - previous_count} new questions!\n"
    )
    return questions
else:
    print()
```
</details>

<details>
<summary><strong>2. View statistics of questions based on profile</strong></summary>

```python
def view_statistics(questions: list[Question], profile: Profile) -> None:
```

1. Asks the user to select ordering type (ascending or descending):
```python
order = user_input_helper.get_order_type()
```
2. Orders all data based on the score and ordering type:
```python
data.sort(key=lambda x: x[5], reverse=reverse_order)
```
3. Prints out nicely formatted table:
```python
columns = [
    "Question ID",
    "Title",
    "Answer",
    "is_enabled",
    "Times_answered",
    "Score (%)",
]
print(tabulate(data, headers=columns, tablefmt="grid"))
print()
```

</details>

<details>
<summary><strong>3. Disable/enable questions</strong></summary>

```python
def disable_or_enable_questions(questions: list[Question]) -> None:
```

1. Prints out all the questions and its data:
```python
data = [[q.id, q.title, q.answer, q.is_enabled] for q in questions]
columns = ["id", "title", "answer", "is_enabled"]
print(tabulate(data, headers=columns, tablefmt="grid"))
```
2. Asks user to enter question id and enables/disables it:
```python
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
```
3. Prints out nicely formatted table of questions and its data with updated enabled/disabled status:
```python
print(
    f"\nSuccessfully changed question {question_id} is_enabled status to {not data[index][3]}\n"
)
```

</details>

<details>
<summary><strong>4. Practice mode for practicing</strong></summary>

```python
def practice_mode(questions: list[Question], profile: Profile) -> None:
```

1. Checks if the are enough questions in total and if there are enough enabled questions to start the Practice Mode:
```python
if not question_helper.is_enough_questions(questions, "Practice"):
    return
elif not question_helper.is_enough_enabled_questions(questions, "Practice"):
    return
```
2. Provides user with questions until the user writes "done".

</details> 

<details>
<summary><strong>5. Test mode for testing one's knowledge</strong></summary>

```python
def test_mode(questions: list[Question], profile: Profile) -> None:
```

1. Checks if the are enough questions in total and if there are enough enabled questions to start the Test Mode:
```python
if not question_helper.is_enough_questions(questions, "Test"):
    return
elif not question_helper.is_enough_enabled_questions(questions, "Test"):
    return
```
2. Gets test questions based on user wanted questions amount:
```python
test_length = user_input_helper.get_user_test_length(questions)
test_questions = question_helper.get_test_questions(questions, test_length)
correct_answers = 0
```
3. Prints out and exports the result of the test:
```python
game_helper.print_test_results(test_length, correct_answers)
csv_helper.export_test_result(test_length, correct_answers, profile)
```

</details>

<details>
<summary><strong>6. Select profile</strong></summary>

```python
def select_profile(profile: Profile) -> Profile:
```

1. Asks the user if they would want to select or create a profile:
```python
user_choice = user_input_helper.select_profile()
```
2. Profile selection handling is allowed only if the are more than 1 already existing profile:
```python
print("Loading available profiles...")
profiles = csv_helper.load_profile_names()

if len(profiles) <= 1:
    print("Please create more profiles before selecting\n")
    return profile
```
3. User cannot create profile if the entered name is empty or name is only consists of decimal values:
```python
if not profile_name:
    print("Profile name cannot be empty!")
    return False
elif profile_name.isdecimal():
    print("Profile name cannot be a number! Please try again.")
    return False
return True
```

</details>

<details>
<summary><strong>7. Exit the quizly</strong></summary>

```python
print("\nSaving...")
csv_helper.save_questions(questions)
csv_helper.save_question_statistics(profile)
sys.exit("\nThanks for playing!")
```

</details>


## Models

<details>
<summary><strong>Profile</strong></summary>

### Data
- **id** – Unique number for profile for easier access.
- **name** – Name of the profile.
- **question_statistics** – Dictionary of [int, QuestionStatistics]. For storing question statistics for a profile.

</details>

<details>
<summary><strong>Question</strong></summary>

### Data
- **id** – Unique id for a question.
- **title** – The question itself.
- **answer** – The correct answer of the question.
- **is_enabled** – Says if the question is enabled/disabled.
- **choices** – Contains all the choices for the answer if the question is a quiz. If the question is free-form then `choices = None`

</details>

<details>
<summary><strong>Question Statistics</strong></summary>

### Data
- **times_answered** – Contains total amount that the question has been answered by the profile.
- **times_answered_correctly** – Contains total amount that the questions has been answered correctly by the profile.
- **weight** – Maximum weight that the question can have. [0.1;1] is the interval of weight.
- **WEIGHT_INCREMENT** – Value that the weight is incremented or decremented based on if the answer is correct or incorrect.
- **MAX_WEIGHT** – Maximum weight that the question can have.
- **MIN_WEIGHT** – Minimum weight that the question can have.
</details>

## Enumerators

<details>
<summary><strong>QuizlyMode</strong></summary>

### Description
The `QuizlyMode` enumerator defines different modes available in the Quizly application.

### Values

- **ADDING_QUESTIONS (1)** – Allows the user to add new questions to the system.
- **STATISTICS_VIEWING (2)** – Enables the user to view question statistics.
- **DISABLE_OR_ENABLE_QUESTIONS (3)** – Provides the option to enable or disable questions.
- **PRACTICE_MODE (4)** – Starts practice mode, where users can answer questions without scoring.
- **TEST_MODE (5)** – Starts test mode, where users answer questions with scoring.
- **PROFILE_SELECT (6)** – Allows users to select or switch profiles.
- **QUIT (7)** – Exits the application.

</details>

<details>
<summary><strong>QustionType</strong></summary>

### Description
The `QuestionType` enumerator defines different question types in the Quizly application.

### Values

- **QUIZ (1)** – Question with choices to answer.
- **FREE_FORM (2)** – Question with text to answer.

</details>



## Additional modules
```bash 
pip install tabulate
```

[Back to top](#readme)
