from typing import Any, Dict, List
from haystack import component, default_from_dict, default_to_dict

from creao.core.Dedup import Dedup

@component
class Deduplication:
    def __init__(self):
        self.dedup = Dedup()

    @component.output_types(dedup_list=List[str])
    def run(self, input_texts: List[str]):
        res = self.dedup.execute(input_texts)
        return {"dedup_list":res}
    
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this component to a dictionary.

        :returns:
            The serialized component as a dictionary.
        """
        return default_to_dict(
            self,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Dedup":
        """
        Deserialize this component from a dictionary.

        :param data:
            The dictionary representation of this component.
        :returns:
            The deserialized component instance.
        """
        return default_from_dict(cls, data)