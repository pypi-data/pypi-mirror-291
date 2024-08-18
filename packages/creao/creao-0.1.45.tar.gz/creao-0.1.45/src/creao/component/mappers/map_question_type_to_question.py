from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures


@component
class MapQuestionTypeToQuestion:
    """
    A component mapping question type to question
    """
    def __init__(self, type_of_questions:Dict[str,str]):
        self.type_of_questions = type_of_questions
        self.generator = Generator()

    @component.output_types(documents=List[Document])
    def run(self, question_mapping:List[Dict[str, str]], chunk:str, file_name:str):
        """
        Map question type to question
        :param question_type: The question type to map
        :return: The question
        """
        def process_question_type(item):
            interest_questions = []
            for q_type in item['q_type']:
                if q_type.lower() in self.type_of_questions:
                    questions = self.generator.generate_questions(file_name, chunk, item['interest'], self.type_of_questions[q_type.lower()])
                    interest_questions.extend(questions)
            return interest_questions

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            raw_questions = [question for result in executor.map(process_question_type, question_mapping) for question in result]
            questions = [item for item in raw_questions if item != []]
        documents = []
        for question in questions:
            doc = Document(content=question, meta={"file_name": file_name, "chunk": chunk})
            documents.append(doc)
        return {"documents": documents}
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this component to a dictionary.

        :returns:
            The serialized component as a dictionary.
        """
        return default_to_dict(
            self,
            type_of_questions=self.type_of_questions,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MapQuestionTypeToQuestion":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict