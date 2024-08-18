from typing import List
from haystack import component, default_from_dict, default_to_dict
from creao.core.Generator import *
import concurrent.futures

@component
class RewriteQuestion:
    def __init__(self):
        self.generator = Generator()

    @component.output_types(outputs=List[str])
    def run(self, inputs:List[str], file_name: str, chunk: str):
        def process_question(question):
            return self.generator.conversational_re_write(question, file_name, chunk)['re_written_question']

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            outputs = list(executor.map(process_question, inputs))
        return {"outputs": outputs}
        
    def to_dict(self) -> dict:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RewriteQuestion":
        return default_from_dict(cls, data)