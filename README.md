# Quizly

## Main functions for user

<details>

<summary><h2>1. Adding questions.<h2></summary>
```python
def add_questions(questions: list[Question]) -> None:
```

Function that handles question adding to the CSV file.

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



2. View statistics of questions based on profile
3. Disable/enable questions
4. Practice mode for practicing 
5. Test mode for testing one's knowledge
6. Select profile
7. Exit the quizly


## Models
<details>
<summary><h2>Profile</h2></summary>
<h3>Data</h3>
- <b>id</b> – Unique number for profile for easier access.
- <b>name</b> – Name of the profile.
- <b>question_statistics</b> – Dictionary of [```int QuestionStatistics```]. For storing question statistics for a profile.

</details>

<details>
<summary><h2>Question</h2></summary>
<h3>Data</h3>
- <b>id</b> – Unique id for a question.
- <b>title</b> – The question itself.
- <b>answer</b> – The correct answer of the question.
- <b>is_enabled</b> – Says if the question is enabled/disabled.
- <b>choices</b> – Contains all the choices for the answer if the question is a quiz. If the question is free-form then ```python choices = None```.

</details>

<details>
<summary><h2>Question Statistics</h2></summary>
<h3>Data</h3>
- <b>times_answered</b> – Contains total amount that the question has been answered by the profile.
- <b>times_answered_correctly</b> – Contains total amount that the questions has been answered correctly by the profile.
* <b>weight</b> – Maximum weight that the question can have. [0.1;1] is the interval of weight.
- <b>WEIGHT_INCREMENT</b> – Value that the weight is incremented or decremented based on if the answer is correct or incorrect.
- <b>MAX_WEIGHT</b> – Maximum weight that the question can have.
- <b>MIN_WEIGHT</b> – Minimum weight that the question can have.
</details>


## Additional modules
```bash 
pip install tabulate
```

[Back to top](#readme)
