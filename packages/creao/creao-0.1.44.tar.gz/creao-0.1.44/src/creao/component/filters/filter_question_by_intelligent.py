from typing import List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures

@component
class ItelligentFilter:
    def __init__(self):
        self.intelligent_question_filter = Intelligent_Question_Filter()

    @component.output_types(documents=List[Document])
    def run(self, documents:List[Document]):
        if len(documents) == 0:
            return {"outputs":[]}
        inputs = [doc.content for doc in documents]
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]
        def filter_question(question):
            filter_flag = self.intelligent_question_filter.execute(question, file_name, chunk)
            return question if filter_flag['Type_of_question'] == "Type_A" else None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            filtered_questions = list(executor.map(filter_question, inputs))

        # Filter out any None values from the list of filtered questions
        questions = [q for q in filtered_questions if q is not None]
        docs = []
        for question in questions:
            doc = Document(content=question, meta={"file_name": file_name, "chunk": chunk})
            docs.append(doc)
        return {"documents": docs}
    
    def to_dict(self) -> dict:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ItelligentFilter":
        return default_from_dict(cls, data)
