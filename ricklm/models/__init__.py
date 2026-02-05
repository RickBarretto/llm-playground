from typing import Literal, ClassVar, overload

import attrs

from ricklm.models.capabilities import GeneratesText


__all__ = ["AmadeusVerbo"]


@attrs.frozen
class AmadeusVerbo(GeneratesText):
    owner: ClassVar[str] = "amadeusai"
    _model: ClassVar[str] = "Amadeus-Verbo-FI-Qwen2.5-{size}-PT-BR-Instruct"
    size: Literal["0.5B", "1.5B", "3B", "7B", "14B", "32B", "72B"] = "7B"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)

