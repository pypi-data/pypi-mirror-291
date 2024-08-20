from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures


@component
class MapInterestToQuestionType:
    """
    A component mapping interest to question type
    """
    def __init__(self, type_of_questions:Dict[str,str]):
        self.type_of_questions = type_of_questions
        self.generator = Generator()

    @component.output_types(question_mapping=List[Dict[str, str]])
    def run(self, documents:List[Document]):
        """
        Map interest to question type
        :param interest: The interest to map
        :return: The question type
        """
        if len(documents) == 0:
            return {"question_mapping":[]}
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]
        interests = [doc.content for doc in documents]
        def process_interest(interest):
            mapping = self.generator.extract_compatible_question_type(interest, list(self.type_of_questions.values()), file_name, chunk)['list_of_extractable_types_of_questions']
            return {"interest": interest, "q_type": [m.lower() for m in mapping]}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            question_mapping = list(executor.map(process_interest, interests))
        return {"question_mapping": question_mapping}
        
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
    def from_dict(cls, data: Dict[str, Any]) -> "MapInterestToQuestionType":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)