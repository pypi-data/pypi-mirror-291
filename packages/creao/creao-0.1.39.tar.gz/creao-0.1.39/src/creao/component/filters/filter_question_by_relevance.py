from typing import List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures

@component
class RelevanceFilter:
    def __init__(self, flag: str = "not useful"):
        self.flag = flag
        self.relevance_filter = Relevance_Filter()

    @component.output_types(filtered_res=List[str])
    def run(self, documents:List[Document]):
        if len(documents) == 0:
            return {"filtered_res":[]}
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]
        questions = [doc.content for doc in documents]
        filter_flags = []
        def process_question(question):
            flag = self.relevance_filter.execute(question, file_name, chunk)
            return {"question": question, "flag": flag}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(process_question, questions))

        filter_flags.extend(results)

        # Step 7: Keep only the relevant questions
        relevant_questions = [item['question'] for item in filter_flags if item["flag"]['Your_Decision'].lower() != "not useful"]
        return {"filtered_res": relevant_questions}

    def to_dict(self) -> dict:
        return default_to_dict(self,flag=self.flag)

    @classmethod
    def from_dict(cls, data: dict) -> "RelevanceFilter":
        return default_from_dict(cls, data)