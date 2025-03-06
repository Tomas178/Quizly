from dataclasses import dataclass


@dataclass
class Question:
    id: int
    title: str
    answer: str
    is_enabled: bool = True
    # Stores possible choices for multiple choice questions
    choices: list[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "answer": self.answer,
            "is_enabled": self.is_enabled,
            "choices": self.to_choices_string(),
        }

    def is_quiz(self) -> bool:
        return self.choices is not None and len(self.choices) > 0

    def to_choices_string(self):
        return "|".join(self.choices) if self.choices else ""

    def __str__(self):
        return f"Question: {self.title}\nAnswer: {self.answer}\n Enabled: {self.is_enabled}"
