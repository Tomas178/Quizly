# Quizly

## Main functions for user

<details>

<summary>**1. Adding questions.**</summary>
```python
def add_questions(questions: list[Question]) -> None:
```

Function that handles question adding to the CSV file.

1. User is allowed to choose between quiz and free-form types:
```python question_type = user_input_helper.question_type_selection()```
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



2. View statistics of questions based on profile
3. Disable/enable questions
4. Practice mode for practicing 
5. Test mode for testing one's knowledge
6. Select profile
7. Exit the quizly


## Models
<details>
<summary>**Profile**</summary>
### Data
- **id** – Unique number for profile for easier access.
- **name** – Name of the profile.
- **question_statistics** – Dictionary of [```int QuestionStatistics```]. For storing question statistics for a profile.

</details>

<details>
<summary>**Question**</summary>
### Data
- **id** – Unique id for a question.
- **title** – It is a question basically.
- **answer** – The correct answer of the question.
- **is_enabled** – Says if the question is enabled/disabled.
- **choices** – Contains all the choices for the answer if the question is a quiz. If the question is free-form then ```python choices = None```.

</details>

<details>
<summary>**Question Statistics**</summary>
### Data
- **times_answered** – Contains total amount that the question has been answered by the profile.
- **times_answered_correctly** – Contains total amount that the questions has been answered correctly by the profile.
* **weight** – Maximum weight that the question can have. [0.1;1] is the interval of weight.
- **WEIGHT_INCREMENT** – Value that the weight is incremented or decremented based on if the answer is correct or incorrect.
- **MAX_WEIGHT** – Maximum weight that the question can have.
- **MIN_WEIGHT** – Minimum weight that the question can have.
</details>


## Additional modules
```bash 
pip install tabulate
```

[Back to top](#readme)
