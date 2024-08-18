from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict
from creao.core.prompts import *
from creao.core.Endpoints import OpenAILLM
import json
from creao.core.Generator import POISchema

@component
class ExtractPOI:
    def __init__(self, custom_prompt: str = None):
        self.custom_prompt = custom_prompt
        self.llm = OpenAILLM()

    @component.output_types(list_of_interest=List[str])
    def run(self, personas:List[str], file_name:str, passage:str):
        res_list = []
        for persona in personas:
            prompt = extract_user_interest_prompt.format(
                persona=persona, file_name=file_name, passage=passage
            )
            raw_answer = json.loads(self.llm.invoke(prompt, POISchema))
            res_list.extend(raw_answer["list_of_interest"])
        return {"list_of_interest":res_list}
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this component to a dictionary.

        :returns:
            The serialized component as a dictionary.
        """
        return default_to_dict(
            self,
            custom_prompt=self.custom_prompt,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractPOI":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)