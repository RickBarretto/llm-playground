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

@attrs.frozen
class Gaia(GeneratesText):
    owner: ClassVar[str] = "CEIA-UFG"
    _model: ClassVar[str] = "Gemma-3-Gaia-PT-BR-{size}-it"
    size: Literal["4b"] = "4b"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)


@attrs.frozen
class Tucano(GeneratesText):
    owner: ClassVar[str] = "TucanoBR"
    _model: ClassVar[str] = "Tucano-1b1-Instruct"
    size: Literal["1.1B", "2.4B"] = "2.4B"

    def _normalize_size(self, size: str) -> str:
        assert size.endswith("B"), "Size must end with 'B'"
        if "." in size:
            return size.replace("B", "").replace(".", "b")
        else:
            return size.replace("B", "b")

    @property
    def model(self) -> str:
        size = self._normalize_size(self.size)
        return self._model.format(size=size)