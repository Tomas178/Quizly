from dataclasses import dataclass
from Models.question import Question
from Models.question_statistics import QuestionStatistics


@dataclass
class Profile:
    id: int
    name: str
    question_statistics: dict[
        int, QuestionStatistics
    ]  # Dict structure: [QuestionID, QuestionStatistics]

    def init_statistics(self, questions: list[Question]) -> None:
        # Ensures that statistics are set for all available questions
        if not self.question_statistics:
            self.question_statistics = {}
        if not questions:
            return
        for question in questions:
            if question.id not in self.question_statistics.keys():
                self.question_statistics[question.id] = QuestionStatistics()

    def get_statistics_for_question(self, question_id: int) -> QuestionStatistics:
        return self.question_statistics.get(question_id)
