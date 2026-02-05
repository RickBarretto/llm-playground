from functools import  lru_cache
from typing import ClassVar

import attrs
from transformers import pipeline

@attrs.frozen
class Model:
    owner: ClassVar[str]
    _model: ClassVar[str]

    @property
    def model(self) -> str:
        return self._model
    
    @property
    def id(self) -> str:
        return f"{self.owner}/{self.model}"

    @property
    def huggginface(self) -> str:
        return f"https://huggingface.co/{self.id}"
    
    @lru_cache(maxsize=None)
    def pipeline(self, task: str) -> str:
        return pipeline(task, model=self.id)
