from typing import Dict, List
from haystack import component, default_from_dict, default_to_dict, Document
from creao.core.Generator import *
import concurrent.futures

@component
class RewriteQuestion:
    def __init__(self):
        self.generator = Generator()

    @component.output_types(documents=List[Document])
    def run(self, documents:List[Document]):
        if len(documents) == 0:
            return {"outputs":[]}
        questions = [doc.content for doc in documents]
        file_name = documents[0].meta["file_name"]
        chunk = documents[0].meta["chunk"]
        def process_question(question):
            return self.generator.conversational_re_write(question, file_name, chunk)['re_written_question']

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            outputs = list(executor.map(process_question, questions))
        docs = []
        for question in outputs:
            doc = Document(content=question, meta={"file_name": file_name, "chunk": chunk})
            docs.append(doc)
        return {"documents": docs}
        
    def to_dict(self) -> dict:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RewriteQuestion":
        return default_from_dict(cls, data)

@component
class PersonaToWritingStyle:
    def __init__(self):
        self.generator = Generator()

    @component.output_types(outputs=List[Dict[str, str]])
    def run(self, personas:List[str]):
        writing_styles = []
        for persona in personas:
            style = json.loads(self.generator.writing_style(persona).strip())
            writing_styles.append({"persona": persona, "style": style['writing_style']})
        return {"outputs": writing_styles}
        
    def to_dict(self) -> dict:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PersonaToWritingStyle":
        return default_from_dict(cls, data)    

@component
class RewriteQuestionByPersona:
    def __init__(self):
        self.generator = Generator()

    @component.output_types(documents=List[Document])
    def run(self, documents:List[Document], writing_styles:List[Dict[str,str]]):
        questions = [doc.content for doc in documents]
        def process_question(question):
            question_variants = []
            for style in writing_styles:
                re_write = self.generator.persona_rewrite(style['style'], question)
                question_variants.append({"new_question": re_write, "style": style, "original_question": question})
            return question_variants

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            re_written_questions = [variant for result in executor.map(process_question, questions) for variant in result]
        docs = []
        for question in re_written_questions:
            doc = Document(content=question['new_question'], meta={"file_name": documents[0].meta["file_name"], "chunk": documents[0].meta["chunk"], "style": question['style'], "original_question": question['original_question']})
            docs.append(doc)
        return {"documents": docs}
        
    def to_dict(self) -> dict:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RewriteQuestionByPersona":
        return default_from_dict(cls, data)